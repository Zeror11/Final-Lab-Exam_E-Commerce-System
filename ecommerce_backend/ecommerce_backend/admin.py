from django.contrib import admin
from .models import User, Product, Order, OrderItem, CheckoutTransaction
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_customer', 'is_employee', 'is_staff')
    list_filter = ('is_customer', 'is_employee', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_customer', 'is_employee')}),
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_ordered')
    inlines = [OrderItemInline]

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'transaction_date', 'total_amount')

admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(CheckoutTransaction, CheckoutAdmin)
