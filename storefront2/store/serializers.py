from rest_framework import serializers
from .models import Product
from decimal import Decimal
from .models import Collection


# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]
    
    products_count = serializers.IntegerField()


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length = 255)
#     description = serializers.CharField()
#     price = serializers.DecimalField(max_digits=6,decimal_places=2, source="unit_price")
#     # added custom field
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
#     # Adds the collection field pk of collection
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset=Collection.objects.all()
#     # )
    
#     # Adds the collection field with value of the __string__ def in collection model
#     collection = serializers.StringRelatedField()

#     # Add object of collection here
#     collection = CollectionSerializer()

#     # Adds hyperlink to the route for collection
#     # collection = serializers.HyperlinkedRelatedField()
    
#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal(1.05)
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "description", "unit_price", "collection", "price_with_tax"]
        
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.05)