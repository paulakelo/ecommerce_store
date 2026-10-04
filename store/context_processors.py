from .models import Category


def store_categories(request):
	cart = request.session.get("cart", {})
	try:
		cart_item_count = sum(max(0, int(quantity)) for quantity in cart.values())
	except (AttributeError, TypeError, ValueError):
		cart_item_count = 0
	return {
		"store_categories": Category.objects.order_by("name"),
		"cart_item_count": cart_item_count,
	}
