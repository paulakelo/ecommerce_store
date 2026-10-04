(() => {
    const summary = document.querySelector(".order-summary");
    const countySelect = document.querySelector("#id_county");
    const shippingValue = document.querySelector("#shipping-cost-value");
    const totalValue = document.querySelector("#order-total-value");

    if (!summary || !countySelect || !shippingValue || !totalValue) {
        return;
    }

    const subtotalCents = Math.round(Number(summary.dataset.subtotal) * 100);
    const formatKes = (amount) =>
        `KES ${amount.toLocaleString("en-KE", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        })}`;

    const updateTotals = () => {
        const option = countySelect.selectedOptions[0];
        const shipping = Number(option?.dataset.shipping || 0);
        shippingValue.textContent = option?.value ? formatKes(shipping) : "Choose county";
        totalValue.textContent = formatKes((subtotalCents + shipping * 100) / 100);
    };

    countySelect.addEventListener("change", updateTotals);
    updateTotals();
})();
