from django.contrib import admin

from products.models import AdditionalInformation, Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount', 'stock_quantity', 'product_ref', 'created_at')
    search_fields = ('name', 'category', 'sku')
    list_filter = ('category', 'created_at')
    prepopulated_fields = {'product_ref': ('name', 'sku')}

    class AdditionalInformationInline(admin.TabularInline):
        model = AdditionalInformation
        extra = 1
    
    inlines = [AdditionalInformationInline]
    

@admin.register(AdditionalInformation)
class AdditionalInformationAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value')
    search_fields = ('product__name', 'key', 'value')