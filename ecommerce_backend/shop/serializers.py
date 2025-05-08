from rest_framework import serializers
from .models import User, Product, Order, OrderItem, CheckoutTransaction

# ------------------- USER --------------------------

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_customer', 'is_employee', 'is_staff', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_role(self, obj):
        return 'employee' if obj.is_employee else 'customer'

# ------------------- PRODUCT -----------------------

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)  # Make image optional for PATCH

    class Meta:
        model = Product
        fields = '__all__'

# ------------------- ORDER ITEM --------------------

# READ: Include product name and price
class OrderItemReadSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='product.price')
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity']

# WRITE: For incoming order creation
class OrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

# ------------------- ORDER -------------------------

# READ: Include nested item details
class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'date_ordered', 'items']

# WRITE: Create with nested items
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

# ------------------- CHECKOUT ----------------------

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

# ------------------- ORDER HISTORY -----------------

class OrderItemHistorySerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'price', 'quantity']

class OrderHistorySerializer(serializers.ModelSerializer):
    items = OrderItemHistorySerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'date_ordered', 'items', 'total']

    def get_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())
