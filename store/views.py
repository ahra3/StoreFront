from django.shortcuts import get_object_or_404
from django.http import HttpRequest,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import ProductSerializer


@api_view()
def product_list(request): # this is a view function
    queryset =Product.objects.select_related('collection').all() #bring all the products from the database
    serializer = ProductSerializer(
        queryset, many=True, context={"request": request}) #serialize the queryset,  we use many=True when  serializing multiple objects
    return Response(serializer.data) #return the serialized data


@api_view()
def product_detail(request,id):
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
@api_view()
def collection_detail(request,pk):
    #collection=get_object_or_404(Collection,id=id)
    return Response('ok')
