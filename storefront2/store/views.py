from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework.request import Request 
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models.aggregates import Count

from rest_framework.views import APIView

# Create your views here.


class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related("collection").filter()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 1:
            return Response({"error": "cannot delete product while there is order for them"})
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        
        
class CollectionList(APIView):
    def get(self, request):
        collections = Collection.objects.annotate(products_count=Count("product")).filter()
        serializer = CollectionSerializer(collections, many=True, context={"request": request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class CollectionDetail(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count("product")), pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    def put(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count("product")), pk=pk)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")), pk=pk)
        if collection.products.count() > 1:
            return Response({"error": "Couldn't delete collection with existing products"})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
