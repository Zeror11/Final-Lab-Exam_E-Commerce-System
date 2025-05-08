from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, User, Order, CheckoutTransaction
from .serializers import (
    ProductSerializer,
    UserSerializer,
    OrderReadSerializer,
    OrderWriteSerializer,
    CheckoutSerializer,
)

# ✅ Decrease stock API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decrease_stock(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        if product.stock > 0:
            product.stock -= 1
            product.save()
            return Response({'message': 'Stock updated', 'stock': product.stock})
        else:
            return Response({'error': 'Out of stock'}, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

# ✅ Return current user info
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# ✅ Product viewset with delete restriction
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.order_items.exists():
            return Response({'error': 'Cannot delete product already ordered.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

# ✅ Order viewset
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return OrderWriteSerializer
        return OrderReadSerializer

# ✅ Checkout transaction viewset
class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = CheckoutTransaction.objects.all()
    serializer_class = CheckoutSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(transaction_date__date=date)
        return queryset

# ✅ Register endpoint
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
