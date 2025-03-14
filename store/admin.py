from django.contrib import admin,messages
from . import models
from django.db.models import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse



# class to create a filter based on the inventory of the product:

class InventoryFilter(admin.SimpleListFilter):
    title='inventory'
    parameter_name='inventory'
    
    # the options of the filter:
    def lookups(self, request, model_admin):
        return [
            ('<10','Low'),
            ('>=10','OK')
        ]
        
    def queryset(self, request, queryset):
        if self.value()=='<10':
            return queryset.filter(inventory__lt=10)
        return queryset.filter(inventory__gt=10)

#Inlining Generic Types : 

    
    
    
#Use ProductAdmin  to manage Product instances ( register the model then customize it ) :
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields=['collection']
    search_fields=['title','description']
    prepopulated_fields={
        'slug':['title']
    }
    actions=['clear_inventory']
    list_display=['title', 'unit_price','inventory_status','collection_title']
    list_editable=['unit_price']
    list_per_page=10
    list_filter=['collection','last_update',InventoryFilter]
    list_select_related=['collection']

    
    @admin.display(ordering='inventory')
    def inventory_status (self,product):
        if product.inventory <10:
            return 'LOW'
        return'OK'
    
    def collection_title(self,product):
        return product.collection.title
    
    @admin.action(description='clear inventory')
    def clear_inventory (self,request,queryset): # the queryset here represents the selected products from the list
        updated_count=queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.ERROR
        )


#the CUSTOMER ADMIN side :
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields=['first_name','last_name']
    list_display=['first_name','last_name','membership','orders_count']
    list_editable=['membership']
    list_per_page=10
    ordering=['first_name','last_name']
    search_fields=['first_name__istartswith','last_name__istartswith']
    
    @admin.display(ordering='orders_count')
    def orders_count (self,customer):
        url1=(
            reverse('admin:store_order_changelist')
            +'?'
            +urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href ="{}">{}</a>',url1, customer.orders_count)
    
    
    def get_queryset(self, request):
        # Annotate the queryset with the count of orders
        return super().get_queryset(request).annotate(orders_count=Count('order'))


#the COLLECTION ADMIN side :
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields=['title']
    list_display=['title','products_count']
    list_per_page=10
    
    @admin.display(ordering='products_count') # the field used with the ordering method should be existed in the model(wether originally or by overriding the get_queryset method)
    # this method is used to make a clickable link that redirects to the products list  of the collection
    def products_count (self,collection):
        url =(
            reverse('admin:store_product_changelist')# we want the url of the changelist of the products that exist in the store app
            +'?'
            +urlencode({
                'collection__id': str(collection.id)
            })) 
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
    
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )

class OrderItemInline(admin.TabularInline):
    model=models.OrderItem
    autocomplete_fields=['product']
    
    
#the ORDERS ADMIN side :
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemInline]
    autocomplete_fields=['customer']
    list_display=['id','placed_at', 'payment_status','customer_name']
    list_per_page=10
    list_select_related=['customer']
    
    
    
    def customer_name(self,order):
        return f"{order.customer.first_name} {order.customer.last_name}"

