from base.models import *


def products(request):
        products = Products.objects.all()
        return {'products': products}


def cart_item_count(request):
        if request.user.is_authenticated:
                x = CartItems.objects.filter(cart__isPaid = False, cart__user=request.user).count()
                return {'item_count': x}
        else:
                return {'item_count': 0}
    
    
def wish_cart_item_count(request):
        if request.user.is_authenticated:
                y = WishListItems.objects.filter(wishList__user=request.user).count()
                return {'wish_item_count': y}
        else:
                return {'wish_item_count': 0}
        
        
# def cart_item(request):
#         if request.user.is_authenticated:
#                 if Cart.objects.get(user=request.user):
#                         cart_item = Cart.objects.get(user=request.user)
#                         return {'cart_item': cart_item}
#                 else:
#                         return {'cart_item': None}
#         else:
#                 return {'cart_item': None}

def cart_item(request):
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart_item = None
        return {'cart_item': cart_item}
    else:
        return {'cart_item': None}


        
def categoriesNav(request):
        categoriesNav = Category.objects.all()
        return {'categoriesNav': categoriesNav}
                