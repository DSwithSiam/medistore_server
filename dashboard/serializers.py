from rest_framework import serializers
from decimal import Decimal
from .models import OrderHistory, RequestQuote, Cart, CartItem, Wishlist


class WishListSerializer(serializers.ModelSerializer):
    wishlist_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Wishlist
        fields = ["wishlist_id", "user", "products", "created_at"]


class RequestQuoteSerializer(serializers.ModelSerializer):
    quote_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = RequestQuote
        fields = [
            "quote_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "description",
            "created_at",
        ]
        write_only_fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "description",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    cart_item_id = serializers.IntegerField(source="id", read_only=True)
    product_ref = serializers.ReadOnlyField(source="product.product_ref")
    name = serializers.ReadOnlyField(source="product.name")
    price = serializers.ReadOnlyField(source="product.price")
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "cart_item_id",
            "product_ref",
            "name",
            "price",
            "discounted_price",
            "quantity",
        ]

    def get_discounted_price(self, obj):
        return obj.product.get_discounted_price()


class CartSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(source="id", read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "cart_id",
            "items",
            "total_items",
            "subtotal",
            "created_at",
            "updated_at",
        ]

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_subtotal(self, obj):
        total = Decimal("0.00")
        for item in obj.items.select_related("product").all():
            total += Decimal(str(item.product.get_discounted_price())) * item.quantity
        return total


class OrderHistorySerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="id", read_only=True)
    cart = CartSerializer(read_only=True)

    class Meta:
        model = OrderHistory
        fields = ["order_id", "cart", "ordered_at"]
