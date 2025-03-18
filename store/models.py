from django.db import models
from django.core.validators import MinValueValidator

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
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    # the choices array gives us a dropdown LIST to choose from:
    membership=models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    #class Meta:
    class Meta:
        ordering=['first_name','last_name']
    

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
    created_at=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField()

class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-date']

