from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2","email","first_name","last_name"),
            },
        ),
    )


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