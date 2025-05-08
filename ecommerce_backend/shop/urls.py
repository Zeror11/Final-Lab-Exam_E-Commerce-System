from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import customer_order_history

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'checkouts', views.CheckoutViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.CurrentUserView.as_view(), name='current-user'),
    path('products/<int:product_id>/decrease-stock/', views.decrease_stock, name='decrease-stock'),
    path('products/<int:product_id>/increase-stock/', views.increase_stock, name='increase-stock'),
    path('orders/history/', customer_order_history, name='order-history'),  # ✅ This must be here
]
