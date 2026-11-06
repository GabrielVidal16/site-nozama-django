from django.contrib import admin
from .models import Product, Purchase, UserProfile

admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(UserProfile)
