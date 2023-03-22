
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from base.forms import CustomUserForm, EditProfileForm, UserForm
from .models import *
from .filters import ListingFilter
import random
from django.contrib.auth.models import User
from django.contrib import messages


from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.views import generic
# Create your views here.

# def main(request):
#     if request.user.is_authenticated:
#         if Cart.objects.get(user = request.user):
#             cart = Cart.objects.get(user = request.user)
#             context = {'cart':cart}
            
#     return render(request, 'main.html', context)




def home(request):
    categories = Category.objects.all()
    items = Products.objects.filter(forDisplay=True)

    coupons = Coupon.objects.filter(is_expired=False)
    
    # images = MultipleImage.objects.all()
    context = {'categories':categories, 'items':items, 'coupons':coupons}
    
    # if Cart.objects.get(user = request.user):
    #     context = {'categories':categories, 'items':items, 'cart':Cart.objects.get(user = request.user)}
    
    
    return render(request, 'index.html', context)


def products(request, pk):
    category = Category.objects.get(uid = pk)
    
    items = Products.objects.filter(category=category)
    items_filter = ListingFilter(request.GET, queryset=items)
    # images = MultipleImage.objects.all()
    
    context = {"items": items_filter}
    
    # if Cart.objects.get(user = request.user):
    #     context = {"items": items_filter, 'cart':Cart.objects.get(user = request.user)}
        
    return render(request, "products.html", context)


from django.db.models import Count
from django.db.models import Q

def productsInfo(request, pk):
    item = Products.objects.get(uid = pk)
    images = MultipleImage.objects.all()
    categoryName = item.category
    
    len_products = len(Products.objects.filter(category = categoryName))
    
    # relatedProducts = Products.objects.filter(category = categoryName)[random.randint(0, int((len_products/2))):random.randint( int(((len_products/2)+1)), int((len_products+1)))]
    related_products = item.get_related_products()

    productSize = item.sizeExtras.all()
    productColor = item.colorExtras.all()
    
    reviews = Review.objects.filter(product=item).order_by('-created_at')
    num_reviews = reviews.count()
    average_rating = item.get_average_rating()
    if request.method == 'POST':
        add_review(request, pk)
        
    rating_summary = reviews.aggregate(
        star1=Count('rating', filter=Q(rating=1)),
        star2=Count('rating', filter=Q(rating=2)),
        star3=Count('rating', filter=Q(rating=3)),
        star4=Count('rating', filter=Q(rating=4)),
        star5=Count('rating', filter=Q(rating=5)),
    )

    
    context = {'rating_summary': rating_summary, 'average_rating': average_rating, 'num_reviews': num_reviews, 'reviews':reviews, 'item': item, 'images':images, 'products': related_products,'productSize':productSize,'productColor':productColor}
    
    # if Cart.objects.get(user = request.user):
    #     context = {'item': item, 'images':images, 'products': relatedProducts[:4], 'cart':Cart.objects.get(user = request.user)}
    
    return render(request, "productInfo.html", context)


def logIn(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already Logged in")
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('name')
            psw = request.POST.get('password')

            user = authenticate(request,username=username, password=psw)
            print(username)
            print(psw)
            print(user)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect('./')
            else:
                messages.warning(request,"Invalid Email or Password")
                return redirect('.')


    return render(request, 'logIn.html')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, "You activated your account, Thx!")
        return redirect("logIn")
    
    else:
        messages.error(request, "Invalid activation link")
        
    return redirect('users-home')


def activateEmail (request, user, to_email):
    mail_subject = "Activate Your Account on e-commerce"
    message = render_to_string("template_active.html",{
                               'user': user,
                               'domain': get_current_site(request).domain,
                               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                               'token': account_activation_token.make_token(user),
                               "protocol": 'https' if request.is_secure() else 'http'
    })
    
    email = EmailMessage(mail_subject, message, to=[to_email])
    
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
        received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check your email please!')


def signUp(request):

    form = CustomUserForm()

    if request.method == "POST":
        
        form = CustomUserForm(request.POST)
        if form.is_valid():
            
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            
            phoneNumber = form.cleaned_data.get("phoneNumber")
            country = form.cleaned_data.get("country")
            gender = form.cleaned_data.get('gender') 
            
            user = User.objects.filter(email=email)
            # inactive_user = send_verification_email(request, form)
            if user.exists():
                messages.warning(request, "Email is already taken")
                return HttpResponseRedirect(request.path_info)
            
            print(country)
            print(gender)
            print(phoneNumber)

            user = User.objects.create(first_name=first_name,last_name=last_name, username=username, email=email)
            user.is_active = False
            user.set_password(password)
            user.save()
            
            addInfo = AdditionalUserInfo.objects.create(user=user, country=country, phoneNumber=phoneNumber, gender=gender)
            addInfo.save()
            
            activateEmail(request, user, form.cleaned_data.get('email'))
            print(user)
            print(user.password)
            messages.success(request, "Created Successfully")
            return redirect("home")
    else:
        form = CustomUserForm()
    return render(request,'signUp.html', {"form":form})


def logOut(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect('./')


def profile(request):
    user = request.user
    userInfo = AdditionalUserInfo.objects.get(user=user)
    
    context = {'userInfo':userInfo}
    
    # if Cart.objects.get(user = request.user):
    #     context = {'userInfo':userInfo, 'cart':Cart.objects.get(user = request.user)}
    
    return render(request, "profileInfo.html", context)


def editProfile(request):
    user = request.user
    userInfo = AdditionalUserInfo.objects.get(user=user)
    form = UserForm(instance=userInfo)
    
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=userInfo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    context = {'userInfo':userInfo, 'form':form}
    
    # if Cart.objects.get(user = request.user):
    #     context = {'userInfo':userInfo, 'form':form, 'cart':Cart.objects.get(user = request.user)}
    
    return render(request, "editProfile.html", context)


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')



def password_success(request):
    # if Cart.objects.get(user = request.user):
    #     return render(request, 'password_success.html', {'cart':Cart.objects.get(user = request.user)})
    return render(request, 'password_success.html', {})


def add_to_wish_list(request, uid):
    
    item = Products.objects.get(uid = uid)
    user = request.user
    
    
    wish_list , _ = WishList.objects.get_or_create(user = user)
    wish_list_item = WishListItems.objects.create(wishList=wish_list, item=item, )

    wish_list_item.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def wishList(request):
    try:
        context = {'cartWish': WishList.objects.get(user = request.user)}
        # if Cart.objects.get(user = request.user):
        #     context = {'cartWish': WishList.objects.get(user = request.user), 'cart':Cart.objects.get(user = request.user)}
        return render(request, 'wishList.html', context)
    except Exception as e:
        print(e)
        return render(request, 'wishList.html')
    
    
    
def remove_wish_list(request, wish_list_item_uid):
    try:
        wish_item = WishListItems.objects.get(uid = wish_list_item_uid)
        wish_item.delete()
    except Exception as e:
        print(e)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

  

def add_to_cart(request, uid):
    
    item = Products.objects.get(uid = uid)
    user = request.user 
    
    quantity = 1
    # selected_size = None
    if request.method=="POST":
        quantity = int(request.POST.get('quantity'))
        # selected_size = request.POST.get('selected_size')
        # print(selected_size)

    # if quantity > item.quantity:
    #     messages.error(request, 'Insufficient quantity.')
    #     return redirect('productsInfo', pk=item.uid)
    
    cart , _ = Cart.objects.get_or_create(user = user)
    cart_item = CartItems.objects.create(cart=cart, item=item, )
    cart_item.quantity = quantity
    # cart_item.size = selected_size
    
    cart_item.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid = cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    try:
        cart_obj = Cart.objects.get(user = request.user)
        if request.method == 'POST':
            coupon = request.POST.get('coupon_code')
            coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
            
            if not coupon_obj.exists():
                messages.warning(request, "Invalid Coupon")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if cart_obj.coupon:
                messages.warning(request, "Coupon is already applied")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            
            if cart_obj.get_total_price() < coupon_obj[0].minimum_amount:
                messages.warning(request, f"The total amount should be greater than {coupon_obj[0].minimum_amount}")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            
            if coupon_obj[0].is_expired:
                messages.warning(request, "The coupon code has been expired")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            cart_obj.coupon = coupon_obj[0]
            cart_obj.save()
            
            messages.success(request, "Coupon applied successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        context = {'cart':cart_obj}
        return render(request, 'cart.html', context)
    except Exception as e:
        print(e)
        return render(request, 'cart.html')
    
    
def remove_coupon(request, cart_uid):
    cart = Cart.objects.get(uid=cart_uid)
    cart.coupon = None
    cart.save()
    
    messages.success(request, "Coupon removed")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    


def checkout(request):
    try:
        cart_obj = Cart.objects.get(user = request.user)
        if request.method == 'POST':
            coupon = request.POST.get('coupon_code')
            coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
            
            if not coupon_obj.exists():
                messages.warning(request, "Invalid Coupon")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if cart_obj.coupon:
                messages.warning(request, "Coupon is already applied")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            
            if cart_obj.get_total_price() < coupon_obj[0].minimum_amount:
                messages.warning(request, f"The total amount should be greater than {coupon_obj[0].minimum_amount}")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            
            if coupon_obj[0].is_expired:
                messages.warning(request, "The coupon code has been expired")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            cart_obj.coupon = coupon_obj[0]
            cart_obj.save()
            
            messages.success(request, "Coupon applied successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        context = {'cart':cart_obj}
        return render(request, 'checkout.html', context)
    except Exception as e:
        print(e)
        return render(request, 'checkout.html')
    
    
def deals(request):
    onlyOfferProduct = SpecialOffer.objects.all()
    categories = Category.objects.all()
    items = Products.objects.filter(views__gte=1000).order_by('-views')[:4]
    images = MultipleImage.objects.all()
    # categoriesT = Category.objects.all()
    # itemsT = Products.objects.filter(forDisplay=True)
    
    oneOffer = OneDayOffer.objects.all()
    
    categoriesT = Category.objects.all()
    products_by_category = {}
    for category in categoriesT:
        itemsT = category.get_first_4_products()
        products_by_category[category] = itemsT

    
    context = {'products_by_category': products_by_category, 'oneOffer':oneOffer, 'onlyOfferProduct':onlyOfferProduct, 'categories':categories, 'items':items, 'categoriesT':categoriesT, 'itemsT':itemsT, 'images':images}
    
    # if Cart.objects.get(user = request.user):
    #     context = {'onlyOfferProduct':onlyOfferProduct, 'categories':categories, 'items':items, 'categoriesT':categoriesT, 'itemsT':itemsT, 'cart':Cart.objects.get(user = request.user)}
    
    return render(request, 'deals.html', context)




def add_review(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            rating = request.POST['rating']
            text = request.POST['text']
            product = Products.objects.get(uid=pk)
            review = Review.objects.create(user=request.user, product=product, rating=rating, text=text)
            return redirect('productsInfo', pk=pk)
    else:
        return redirect('logIn')

