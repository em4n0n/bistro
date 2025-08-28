from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Category, MenuItem, Order
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer
from .permissions import IsAdminOrReadOnly

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.filter(is_availabe=True).select_related('category').order_by('name')
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category_name']
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('items_menu_item')
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['list', 'update', 'partial_update', 'destroy', 'set_status']:
            return [IsAuthenticated()]
        return []
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return qs.order_by('-created_at')
        if user.is_authenticated:
            return qs.filter(user=user).order_by('-created_at')
        return qs.none()

    @action(detail=True, methods=['post'])
    def set_status(self, request, pk=None):
        order = self.get_object()
        if not request.user.is_staff:
            return Response({'detail': 'Forbidden'}, status=403)
        status_value = request.data.get('status')
        valid = dict(Order.STATUS_CHOICES)
        if status_value not in valid:
            return Response({'detail': 'Invalid status'}, status=400)
        order.status = status_value
        order.save(update_fields=['status'])
        return Response(self.get_serializer(order).data)