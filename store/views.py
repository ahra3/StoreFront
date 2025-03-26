from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,ListModelMixin,UpdateModelMixin
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import Product,Collection,Review,Cart,CartItem
from .fliters import ProductFilter
from .pagination import DefaultPagination
from .serializers import ProductSerializer, CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer


class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    pagination_class=DefaultPagination
    search_fields=['title','description']
    ordering_fields=['unit_price','last_update']

    
    
    def get_serializer_context(self):
        return {"request":self.request}
    
    def destroy(self, request, *args, **kwargs):#this method enable deleting only  when we look for the id of one  product
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'Product cannot be deleted because it is associated with an order item '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    
    

class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class=CollectionSerializer
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count()>0:
            return Response({'error':'Collection cannot be deleted because it contains products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    
    """
        here we are overriding the get_serializer_context method
        to pass the product_id to the serializer
        
    """
    def get_serializer_context(self): # we extract the product_id from the views page bcz it where the url is applied 
        return {'product_id':self.kwargs['product_pk']}
    
    """
        here we are overriding the get_queryset method
        to list only the reviews of the product with the id in the url
        
    """
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

class CartViewSet(CreateModelMixin,
                RetrieveModelMixin,
                DestroyModelMixin,
                GenericViewSet):
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer

class CartItemViewSet(ModelViewSet):
    # this attribute is to determine the methods allowed(no put) :
    http_method_names=['get','post','patch','delete']
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    def get_queryset(self):
        return CartItem.objects \
                .filter(cart_id=self.kwargs['cart_pk'])\
                .select_related('product')
    
    def get_serializer_class(self): # it's to decide which serialize we are gonna use since ,we have more than one 
        if self.request.method=='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer