from django.contrib import admin

from e_shop.models import Category, Product, SubCategory, Cart, CartItem, ProductVariant, Size, Color

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(SubCategory)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ProductVariant)
admin.site.register(Color)
admin.site.register(Size)