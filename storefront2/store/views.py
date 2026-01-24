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
from rest_framework.viewsets import ModelViewSet

# Create your views here.



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 1:
            return Response({"error": "cannot delete product while there is order for them"})
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).filter()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")), pk=pk)
        if collection.products.count() > 1:
            return Response({"error": "Couldn't delete collection with existing products"})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
