(() => {
    const summary = document.querySelector(".order-summary");
    const form = document.querySelector("[data-cart-form]");
    const countySelect = document.querySelector("#id_county");
    const shippingValue = document.querySelector("#shipping-cost-value");
    const totalValue = document.querySelector("#order-total-value");
    const subtotalValue = document.querySelector("[data-subtotal-value]");
    const updateStatus = document.querySelector("#cart-update-status");

    if (!summary || !form || !countySelect || !shippingValue || !totalValue) {
        return;
    }

    let subtotalCents = Math.round(Number(summary.dataset.subtotal) * 100);
    let saveTimer;
    const locale = document.documentElement.lang.startsWith("sw") ? "sw-KE" : "en-KE";
    const formatKes = (amount) =>
        `KES ${amount.toLocaleString(locale, {
            maximumFractionDigits: 0,
        })}`;

    const updateTotals = () => {
        const option = countySelect.selectedOptions[0];
        const shipping = Number(option?.dataset.shipping || 0);
        shippingValue.textContent = option?.value
            ? formatKes(shipping)
            : summary.dataset.messageChooseCounty;
        totalValue.textContent = formatKes((subtotalCents + shipping * 100) / 100);
    };

    const setStatus = (message, isError = false) => {
        if (!updateStatus) return;
        updateStatus.textContent = message;
        updateStatus.classList.toggle("is-error", isError);
    };

    const applyCart = (cart) => {
        subtotalCents = Math.round(Number(cart.subtotal) * 100);
        summary.dataset.subtotal = cart.subtotal;
        if (subtotalValue) subtotalValue.textContent = formatKes(Number(cart.subtotal));
        cart.items.forEach((item) => {
            const row = document.querySelector(`[data-cart-item="${item.id}"]`);
            if (!row) return;
            const input = row.querySelector(".order-quantity");
            const lineTotal = row.querySelector("[data-line-total]");
            if (input) input.value = item.quantity;
            if (lineTotal) lineTotal.textContent = formatKes(Number(item.line_total));
        });
        updateTotals();
    };

    const saveQuantities = async () => {
        setStatus(summary.dataset.messageSaving);
        try {
            const response = await fetch(summary.dataset.updateUrl, {
                method: "POST",
                headers: { "X-Requested-With": "XMLHttpRequest" },
                body: new FormData(form),
            });
            const cart = await response.json();
            applyCart(cart);
            if (!response.ok) {
                setStatus(cart.errors[0] || summary.dataset.messageUnableToUpdate, true);
                return;
            }
            setStatus(summary.dataset.messageQuantitiesSaved);
        } catch (error) {
            setStatus(summary.dataset.messageCouldNotSave, true);
        }
    };

    document.querySelectorAll(".order-quantity").forEach((input) => {
        input.addEventListener("input", () => {
            const value = Number(input.value);
            const minimum = Number(input.min || 1);
            const maximum = Number(input.max);
            if (!Number.isInteger(value) || value < minimum || value > maximum) {
                const rangeMessage = summary.dataset.messageQuantityRange
                    .replace("__minimum__", minimum)
                    .replace("__maximum__", maximum);
                setStatus(rangeMessage, true);
                return;
            }
            const row = input.closest("[data-cart-item]");
            const unitPrice = Number(row.dataset.unitPrice);
            row.querySelector("[data-line-total]").textContent = formatKes(unitPrice * value);
            subtotalCents = Array.from(document.querySelectorAll("[data-cart-item]")).reduce(
                (total, item) => total + Math.round(Number(item.dataset.unitPrice) * Number(item.querySelector(".order-quantity").value || 0) * 100),
                0
            );
            if (subtotalValue) subtotalValue.textContent = formatKes(subtotalCents / 100);
            updateTotals();
            setStatus(summary.dataset.messageSaving);
            clearTimeout(saveTimer);
            saveTimer = setTimeout(saveQuantities, 450);
        });
    });

    countySelect.addEventListener("change", updateTotals);
    updateTotals();
})();
