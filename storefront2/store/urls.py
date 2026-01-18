from django.urls import path
from .views import ProductDetail, ProductList,CollectionList, CollectionDetail

urlpatterns = [
    path("products/", ProductList.as_view()),
    path("products/<int:id>/", ProductDetail.as_view()),
    path("collections/", CollectionList.as_view()),
    path("collections/<int:pk>/", CollectionDetail.as_view()),
]


