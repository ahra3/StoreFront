from itertools import count
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import HttpRequest,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import ProductSerializer, CollectionSerializer


@api_view(['GET','POST'])
def product_list(request): # this is a view function
    if request.method=='GET':
        queryset =Product.objects.select_related('collection').all() #bring all the products from the database
        serializer = ProductSerializer(
        queryset, many=True, context={"request": request}) #serialize the queryset,  we use many=True when  serializing multiple objects
        return Response(serializer.data) #return the serialized data
    elif request.method=='POST':
        #here happens the deserialization:
        serializer=ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        

@api_view(['GET','PUT','DELETE'])
def product_detail(request,id): #this function requires to pass the id of the product
    
    product = get_object_or_404(Product, id=id)
    
    if request.method=='GET': #serialize the product
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method=='PUT':#deserialize the data
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        if product.orderitems.count()>0:
            return Response({'error':'Product cannot be deleted because it si associated with an order item '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



@api_view(['GET','POST'])
def collection_list(request):
    if request.method=='GET':
        queryset=Collection.objects.prefetch_related('products').annotate(products_count=Count('products')).all()
        serializer=CollectionSerializer(queryset,many=True, context={"request": request})
        return Response(serializer.data) # when getting , we return the object data
    elif request.method=='POST':
        serializer=CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) # when creating we return the object data and the status code 201


@api_view(['GET','PUT','DELETE'])
def collection_detail(request,id):
    collection=get_object_or_404(Collection.objects.annotate(products_count=Count('products')),id=id)
    if request.method=='GET':
        serializer=CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        if collection.products.count()>0:
            return Response({'error':'Collection cannot be deleted because it has products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)