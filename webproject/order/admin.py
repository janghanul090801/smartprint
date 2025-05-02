from django.contrib import admin
from .models import Goods,Cart, OrderedCart, PaperType

# Register your models here.

admin.site.register(Goods)
admin.site.register(Cart)
admin.site.register(OrderedCart)
admin.site.register(PaperType)