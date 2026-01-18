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
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

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

    
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).filter()
    serializer_class = CollectionSerializer
    
    def get_serializer_context(self):
        return super().get_serializer_context()
    
    
class CollectionDetail(RetrieveUpdateDestroyAPIView):    
    serializer_class =CollectionSerializer
    queryset = Collection.objects.annotate(products_count=Count("products"))
    

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")), pk=pk)
        if collection.products.count() > 1:
            return Response({"error": "Couldn't delete collection with existing products"})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
