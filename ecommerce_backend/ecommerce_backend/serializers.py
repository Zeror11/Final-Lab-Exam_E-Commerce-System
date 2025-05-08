from rest_framework import serializers
from .models import User, Product, Order, OrderItem, CheckoutTransaction

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_customer', 'is_employee', 'is_staff', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def get_role(self, obj):
        return 'employee' if obj.is_employee else 'customer'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# READ serializer for OrderItem
class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

# WRITE serializer for OrderItem
class OrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

# READ serializer for Order
class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'date_ordered', 'items']

# WRITE serializer for Order
class OrderWriteSerializer(serializers.ModelSerializer):
    items = OrderItemWriteSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'date_ordered', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class CheckoutSerializer(serializers.ModelSerializer):
    order_customer_username = serializers.CharField(source='order.customer.username', read_only=True)

    class Meta:
        model = CheckoutTransaction
        fields = ['id', 'order', 'transaction_date', 'total_amount', 'order_customer_username']
        read_only_fields = ['transaction_date', 'total_amount']

    def create(self, validated_data):
        order = Order.objects.prefetch_related('items__product').get(pk=validated_data['order'].id)
        total = sum([
            item.product.price * item.quantity
            for item in order.items.all()
        ])
        validated_data['total_amount'] = total
        return super().create(validated_data)
