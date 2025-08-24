from rest_framework import serializers
from .models import Category, MenuItem, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all(), write_only=True
    )
    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "price_cents", "is_available", "image", "category", "category_id"]

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        source="menu_item", queryset=MenuItem.objects.all(), write_only=True
    )
    subtotal_cents = serializers.IntegerField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "menu_item", "menu_item_id", "quantity", "price_cents", "subtotal_cents"]
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_cents = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer_name", "customer_phone", "status", "notes", "items", "total_cents", "created_at"]
        read_only_fields = ["status", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        user = self.context["request"].user if self.context["request"].user.is_authenticated else None
        order = Order.objects.create(user=user, **validated_data)
        for item in items_data:
            menu_item = item["menu_item"]
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item.get("quantity", 1),
                price_cents=item.get("price_cents", menu_item.price_cents),
            )
        return order