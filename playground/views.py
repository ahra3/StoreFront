
from django.shortcuts import render
from store.models import Product,Customer,Collection,Order,OrderItem,Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F,Value,Case,When,Func,ExpressionWrapper,DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Avg, Min,Sum
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem,TaggedItemManager
from django.db import transaction
# Create your views here.
def say_hello(request):
    
    #if there is no matching result , it return nothing 
    #product = Product.objects.filter(pk=0).first()
    #queryset=Customer.objects.filter(email__endswith='.com')
    #queryset=Product.objects.filter(
    # Q(inventory__lt=10) & ~Q(unit_price__lt=20))
    #queryset=Product.objects.order_by('unit_price')[0]   

    #queryset=OrderItem.objects.values_list('product__title','order__placed_at','order__payment_status').distinct().order_by('product__title')
    #queryset=Product.objects.filter(id__in=OrderItem.objects.values_list('product_id').distinct()).order_by('title')
    #queryset=Product.objects.select_related('collection').all()
    #queryset=Product.objects.prefetch_related('collection').all()
    #queryset=Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    #result =OrderItem.objects.select_related('product').filter(product_id=1).aggregate(Sum('quantity'))
    #result=Order.objects.select_related('customer').filter(customer_id=1).aggregate(Count('id'))
    #result=Product.objects.select_related('collection').filter(collection_id=3).aggregate(
        #min_price=Min('unit_price'),max_price=Max('unit_price'),average_price=Avg('unit_price')
        # )
    #queryset=Product.objects.annotate(new_unit_price=F('unit_price')+Value(1),is_expensive=Case(When(unit_price__gt=60, then=Value(True)),default=Value(False)))
    #queryset=Customer.objects.annotate(
        #CONCAT/
    #  full_name=Concat('first_name', Value(' '),'last_name')
    #)
    #queryset=Customer.objects.annotate(
        #order_count=Count('order')
    #)
    # queryset=Product.objects.annotate(
    #     discounted_price=ExpressionWrapper(F('unit_price')*0.6, output_field=DecimalField()) 
    #     )
    # queryset=Customer.objects.annotate( last_order_id=Max('order__id'))
    
    
    #content type is a model:
    # queryset=TaggedItem.objects.get_tags_for(Product,1)
    
    
    
    #create an object and insert it in the database:
    # collection=Collection(pk =1)
    # collection.title='News'
    # collection.featured_product=None
    # #save it in the database:
    # collection.save()
    
    
    # but if we want to  update only one field of the collection : 
    #Collection.objects.filter(pk=5484662).update(featured_product=None)
    
    
    
    #deleting an object:
    #Collection.objects.filter(pk=548466).delete()
    
    # with transaction.atomic():
    #     order=Order(pk=1001)
    #     order.customer_id=99
    #     order.save()
        
    #     item=OrderItem(pk=1001)
    #     item.order=order
    #     item.product_id=70
    #     item.quantity=6
    #     item.unit_price=30
    #     item.save()
    
    
    
    
    
    
    
    #we can replace the above code with (problem of must remember the fields):
    #collection=Collection.objects.create(title="podcast",featured_product=Product(66))
    
    

    
    return render(request,'hello.html',{'name':'ZAHRA'})