from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
# create the base database for others to add the uuid
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # Pass super class attributes to the sub-classes
    class Meta:
        abstract = True
        
        
class AdditionalUserInfo(BaseModel):
    class GenreChoices(models.TextChoices):
        male = "male"
        female = "female"
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prof")
    image = models.ImageField(default="defaultImg.png", null=True, blank=True)
    phoneNumber = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GenreChoices.choices, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    

class Category(BaseModel):
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(max_length=1500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")

    
    def __str__(self):
        return self.name
    
    
    def get_first_4_products(self):
        return self.products.order_by('uid')[:3]
    
    # add the slug name automatically
    def save(self, *args, **kwargs):
        # auto generate product slug
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    # the name shown for the database at the admin panel
    class Meta:
        verbose_name_plural = "Category"


class sizeExtras(BaseModel):
    size = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.size
    
    class Meta:
        verbose_name_plural = "sizeExtras"


class colorExtras(BaseModel):
    color = models.CharField(max_length=100, null=False, blank=False)
    hexCode = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.color
    
    class Meta:
        verbose_name_plural = "colorExtras"
        
class Products(BaseModel):
    class GenreChoices(models.TextChoices):
        manual = "manual"
        automatic = "automatic"
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    bio = models.TextField(max_length=200, null=False, blank=False)
    description = models.TextField(max_length=1500, null=False, blank=False)
    filterField = models.CharField(max_length=10, choices=GenreChoices.choices, null=True, blank=True)
    availability = models.BooleanField(default=True)
    imgField = models.CharField(max_length=2083, null=True, blank=True)
    # thumbnailImg = models.CharField(max_length=2083)
    # add_ons_field = 
    isSale = models.BooleanField(default=False)
    salePrice = models.IntegerField(default=0)
    forDisplay = models.BooleanField(default=False)
    related_products = models.ManyToManyField('self', blank=True)
    views = models.IntegerField(default=0)
    sizeExtras = models.ManyToManyField(sizeExtras,blank=True)
    colorExtras = models.ManyToManyField(colorExtras,blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.name
    
    def get_related_products(self):
        return self.related_products.all()
    
    def get_discount_percentage(self):
        if self.isSale:
            discount = (self.price - self.salePrice) / self.price * 100
            return int(discount)
        else:
            return 0
        
        
    def get_average_rating(self):
        reviews = Review.objects.filter(product=self)
        if reviews.count() == 0:
            return 0
        else:
            return sum(review.rating for review in reviews) / reviews.count()
    
    class Meta:
        verbose_name_plural = "Products"

class MultipleImage(BaseModel):
    images = models.CharField(max_length=2083)
    productName = models.ForeignKey(Products, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.productName.name + ' Images'
    class Meta:
        verbose_name_plural = "Multiple Image"
        
        
class WishList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishList')
    
    class Meta:
        verbose_name_plural = "Wish List"
        
        
class WishListItems(BaseModel):
    wishList = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name="wish_list_items")
    item = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_item_price(self):
        price = [self.item.price]
          
        return sum(price)
    
    class Meta:
        verbose_name_plural = "Wish List Item"
        
        
class SpecialOffer(BaseModel):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    timeLeft = models.DateField()
    offerDescription = models.CharField(max_length=1500, null=False, blank=False)
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name_plural = "Product Offer"
        
class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=0)
    minimum_amount = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Coupon"

    
    def __str__(self):
        return str(self.coupon_code)  
        
class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    isPaid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return str(self.user) + " Cart"
    
    def get_total_price(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append((cart_item.item.price*cart_item.quantity))
                         
            
        if self.coupon:
            if self.coupon.minimum_amount < sum(price):
                return sum(price) - self.coupon.discount_price
        
        return sum(price)
    
    
    class Meta:
        verbose_name_plural = "Cart"
        

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50)
    
    def get_item_price(self):
        price = [(self.item.price * self.quantity)]
          
        return sum(price)
    
    class Meta:
        verbose_name_plural = "Cart Item"
        
               
from django.utils import timezone
               
class OneDayOffer(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    end_time = models.DateTimeField() 
    
    
    def __str__(self):
        return self.product.name
    
    @property
    def time_remaining(self):
        now = timezone.now()
        remaining = (self.end_time - now).total_seconds()
        return int(remaining) if remaining > 0 else 0
    
    class Meta:
        verbose_name_plural = "One Day Offer"


    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    rating = models.FloatField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def rating_stars(self):
        full_stars = int(self.rating)
        half_stars = int(round(self.rating - full_stars))
        empty_stars = 5 - full_stars - half_stars
        return '★' * full_stars + '☆' * half_stars + '☆' * empty_stars