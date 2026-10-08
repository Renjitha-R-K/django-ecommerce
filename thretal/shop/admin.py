from django.contrib import admin

from shop.models import Category, Subcategory, Product,ProductImage,CustomUser

# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(CustomUser)