from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(MultipleImage)
admin.site.register(WishList)
admin.site.register(WishListItems)
admin.site.register(AdditionalUserInfo)
admin.site.register(Cart)
admin.site.register(SpecialOffer)
admin.site.register(CartItems)
admin.site.register(Coupon)
admin.site.register(OneDayOffer)
admin.site.register(sizeExtras)
admin.site.register(colorExtras)
admin.site.register(Review)

