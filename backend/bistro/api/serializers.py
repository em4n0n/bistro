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