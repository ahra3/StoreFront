from rest_framework import serializers
from .models import Product,Collection
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title'] #the fields that will appear in the response
        
    


# the function of this class is to both  serialize and deserialize the data
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','slug','inventory','unit_price','price_with_tax','collection'] #the fields that will appear in the response
        
    price_with_tax=serializers.SerializerMethodField(method_name="calculate_tax")
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail',
    # )
    
    
    def calculate_tax(self,product:Product):
        return product.unit_price* Decimal (1.1)
    
    # def validate_title(self,value):
    #     if len(value)<10:
    #         return serializers.ValidationError('the title is too short')
    #     return value
    
    
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','products_count'] #the fields that will appear in the response
        
    products_count=serializers.IntegerField()
    
    # def get_product_count(self,collection:Collection):
    #     return collection.product_set.count()