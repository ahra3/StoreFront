from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product


# Register your models here.
class TagItemInline(GenericTabularInline):
    model=TaggedItem
    autocomplete_fields=['tag']

class CustomProductAdmin(ProductAdmin):
    inlines=[TagItemInline]
    

admin.site.unregister(Product)
#use  the new CustomerProductAdmin class (which already
# inherits everything from the farmer ProductAdmin class) 
# to manage the Product model:
admin.site.register(Product,CustomProductAdmin)