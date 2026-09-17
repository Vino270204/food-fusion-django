from django.contrib import admin

from .models import (
    Restaurant,
    Food,
    Cart,
    CartItem,
    Offer,
    Order,
    OrderItem,
    Payment,
)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "phone",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "location",
    )


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "restaurant",
        "category",
        "price",
        "is_available",
    )

    list_filter = (
        "category",
        "is_available",
        "restaurant",
    )

    search_fields = (
        "name",
        "category",
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "created_at",
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "cart",
        "food",
        "quantity",
    )


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "discount_percentage",
        "coupon_code",
        "start_date",
        "end_date",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
        "coupon_code",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "name",
        "total_amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "food",
        "quantity",
        "price",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "payment_method",
        "amount",
        "status",
        "paid_at",
    )

    list_filter = (
        "payment_method",
        "status",
    )