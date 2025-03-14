from django.shortcuts import get_object_or_404
from django.http import HttpRequest,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import ProductSerializer


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


@api_view(['GET','PUT'])
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



@api_view()
def collection_detail(request,pk):
    #collection=get_object_or_404(Collection,id=id)
    return Response('ok')
