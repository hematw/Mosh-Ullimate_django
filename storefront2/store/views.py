from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework.request import Request 
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models.aggregates import Count

# Create your views here.

@api_view(["GET", "POST"])
def product_list(request: Request):
    if request.method == "GET":
        queryset = Product.objects.select_related("collection").filter()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors)

@api_view(["GET", "PUT", "DELETE"])
def product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    
    if request.method == "GET": 
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    elif request.method == "DELETE":
        if product.orderitem_set.count() > 1:
            return Response({"error": "cannot delete product while there is order for them"})
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
@api_view(["GET", "POST"])
def collection_list(request: Request):
    if request.method == "GET":
        collections = Collection.objects.annotate(products_count=Count("product")).filter()
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


@api_view(["GET", "DELETE", "PUT"])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count("product")), pk=pk)
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        if collection.products.count() > 1:
            return Response({"error": "Couldn't delete collection with existing products"})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)