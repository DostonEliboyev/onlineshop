from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'quantity', 'price', 'subtotal')

    def subtotal(self, obj):
        return obj.subtotal


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'city', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'city')
    list_editable = ('status',)
    search_fields = ('full_name', 'phone', 'address')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
