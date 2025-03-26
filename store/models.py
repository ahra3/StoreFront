from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator
from uuid import uuid4

class Promotion (models.Model):
    description =models.TextField()
    discount=models.FloatField()


class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name="+")
    def __str__(self):
        return self.title
    class Meta:
        ordering=['title']

class Product(models.Model):

    title=models.CharField(max_length=255)
    description=models.TextField()
    slug=models.SlugField()
    unit_price=models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory=models.IntegerField(
        validators=[MinValueValidator(1)]
        )
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.CASCADE,related_name='products')
    promotions=models.ManyToManyField(Promotion,blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering=['title']
    
    
class Customer(models.Model):
    #order_set: the list of all the ordes a customer made
    #THESE VALUES ARE GONNA BE STORED IN THE DATABASE:
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLD='G'
    
    
    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold'),
    ]
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    # the choices array gives us a dropdown LIST to choose from:
    membership=models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering=['user__first_name','user__last_name']
    

class Order(models.Model):
    #orderitem_set:list of the order items.
    PAYMENT_CHOICES=[
        ('P','Pending'),
        ('C','Complete'),
        ('F','Failed'),
    ]
    placed_at=models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=1,choices=PAYMENT_CHOICES,default='P')
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)
    
    class Meta:
        permissions=[
            ('cancel_order','Can cancel order')
        ]
        

class Address (models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    zipi=models.CharField(max_length=6)
    
class OrderItem(models.Model):
    #now we know that each order has a lot of orderitems, now the list of order items
    #in the order model (which is set by default) called: orderitem_set 
    order=models.ForeignKey(Order,on_delete=models.PROTECT)
    product=models.ForeignKey(Product,on_delete=models.PROTECT , related_name='orderitems')
    quantity=models.PositiveBigIntegerField()
    unit_price=models.DecimalField(max_digits=5,decimal_places=2)
    
class Cart(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
    created_at=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(
        validators=[MinValueValidator(1)]
    )
    
    class Meta:
        # this means that the couple cart and product should be unique, no duplicates in the same product in the same cart
        unique_together=['cart','product']

class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-date']

