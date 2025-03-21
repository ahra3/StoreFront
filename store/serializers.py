from rest_framework import serializers
from .models import Product,Collection,Review,Cart,CartItem
from decimal import Decimal




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
        
    products_count=serializers.IntegerField(read_only=True)
    
    # def get_product_count(self,collection:Collection):
    #     return collection.product_set.count()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','date','name','description']
        
    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model=CartItem
        fields=['id','product','quantity','total_price']
    
    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price

class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    items=CartItemSerializer(many=True)
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    
    class Meta:
        model=Cart
        fields=['id','items','total_price']
    def get_total_price(self,cart:Cart):
        return sum(item.quantity * item.product.unit_price for item in cart.items.all())
