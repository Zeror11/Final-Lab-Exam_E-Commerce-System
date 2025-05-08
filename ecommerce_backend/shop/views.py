from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderHistorySerializer
from .models import Order


from .models import Product, User, Order, CheckoutTransaction
from .serializers import (
    ProductSerializer,
    UserSerializer,
    OrderReadSerializer,
    OrderWriteSerializer,
    CheckoutSerializer,
)

# ✅ Customer Order History (GET all orders for the authenticated customer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_order_history(request):
    user = request.user
    orders = Order.objects.filter(customer=user).prefetch_related('items__product')
    serializer = OrderHistorySerializer(orders, many=True)
    return Response(serializer.data)



# ✅ API: Increase product stock
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def increase_stock(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        quantity = int(request.data.get('quantity', 1))
        product.stock += quantity
        product.save()
        return Response({'message': 'Stock increased.'}, status=200)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


# ✅ API: Decrease product stock (by 1)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decrease_stock(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        if product.stock > 0:
            product.stock -= 1
            product.save()
            return Response({'message': 'Stock updated', 'stock': product.stock}, status=200)
        else:
            return Response({'error': 'Out of stock'}, status=400)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)


# ✅ API: Get current user info
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ✅ Product CRUD (with delete restriction if ordered)
from rest_framework.parsers import MultiPartParser, FormParser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]  # <-- ADD THIS

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.order_items.exists():
            return Response({'error': 'Cannot delete product already ordered.'}, status=400)
        return super().destroy(request, *args, **kwargs)


# ✅ Order CRUD with separate read/write serializers
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return OrderWriteSerializer
        return OrderReadSerializer


# ✅ Checkout Transaction CRUD (with optional date filter)
class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = CheckoutTransaction.objects.all()
    serializer_class = CheckoutSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(transaction_date__date=date)
        return queryset


# ✅ User Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
