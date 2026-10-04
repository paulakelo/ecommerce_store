from django.contrib import admin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from .models import (
    Category,
    CustomerMessage,
    Order,
    OrderItem,
    Product,
    PromotionCampaign,
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_available']
    list_filter = ['is_available', 'created', 'updated']
    list_editable = ['price', 'stock', 'is_available']
    prepopulated_fields = {'slug': ('name',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'phone_number', 'payment_status', 'is_paid', 'created']
    list_filter = ['payment_status', 'is_paid', 'created']
    inlines = [OrderItemInline]


@admin.register(CustomerMessage)
class CustomerMessageAdmin(admin.ModelAdmin):
    list_display = ("created", "user", "kind", "title", "sender", "read_at")
    list_filter = ("kind", "created", "read_at")
    search_fields = ("user__username", "user__email", "sender__username", "body")
    readonly_fields = ("created", "read_at", "sender")
    autocomplete_fields = ("user",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.sender = request.user
        super().save_model(request, obj, form, change)


@admin.register(PromotionCampaign)
class PromotionCampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "sent_at")
    readonly_fields = ("created", "sent_at")
    actions = ("send_to_customers",)

    @admin.action(description="Send selected promotions to all active customers")
    def send_to_customers(self, request, queryset):
        User = get_user_model()
        recipients = list(
            User.objects.filter(is_active=True, is_staff=False).only("pk")
        )
        sent_campaigns = 0
        with transaction.atomic():
            campaigns = queryset.select_for_update().filter(sent_at__isnull=True)
            for campaign in campaigns:
                CustomerMessage.objects.bulk_create(
                    [
                        CustomerMessage(
                            user=recipient,
                            kind=CustomerMessage.Kind.PROMOTION,
                            title=campaign.title,
                            body=campaign.body,
                        )
                        for recipient in recipients
                    ]
                )
                campaign.sent_at = timezone.now()
                campaign.save(update_fields=("sent_at",))
                sent_campaigns += 1

        self.message_user(
            request,
            f"Sent {sent_campaigns} promotion(s) to {len(recipients)} active customer(s).",
            messages.SUCCESS,
        )