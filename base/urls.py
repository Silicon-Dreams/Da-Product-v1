from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<pk>', views.products, name='products'),
    path('productsInfo/<pk>', views.productsInfo, name='productsInfo'),
    path('signUp', views.signUp, name='signUp'),
    path('logIn', views.logIn, name='logIn'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('logOut', views.logOut, name='logOut'),
    path('profile', views.profile, name="profile"),
    path('editProfile', views.editProfile, name="editProfile"),
    path('edit-profile-main', views.UserEditView.as_view(), name='edit_profile_main'),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='change-password.html')),
    path('password/', views.PasswordsChangeView.as_view(template_name='change-password.html')),
    path('password_success', views.password_success, name='password_success'),
    path('wishList', views.wishList, name='wishList'),
    path('add-to-wish-list/<uid>/', views.add_to_wish_list, name="add_to_wish_list"),
    path('remove-wish-list/<wish_list_item_uid>/', views.remove_wish_list, name="remove_wish_list"),
    path('deals', views.deals, name='deals'),
    path('add-to-cart/<uid>/', views.add_to_cart, name="add_to_cart"),
    path('cart', views.cart, name='cart'),
    path('remove-cart/<cart_item_uid>/', views.remove_cart, name="remove_cart"),
    path('remove-coupon/<cart_uid>/', views.remove_coupon, name="remove_coupon"),
    path('checkout', views.checkout, name='checkout'),

    path('productsInfo/<pk>/add_review/', views.add_review, name='add_review'),
]