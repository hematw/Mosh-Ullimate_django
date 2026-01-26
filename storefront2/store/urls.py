from django.urls import path
from .views import ProductViewSet, CollectionViewSet, ReviewViewSet
from rest_framework_nested import routers


router = routers.SimpleRouter()
router.register("products", ProductViewSet, basename="products")
router.register("collections", CollectionViewSet)

review_router = routers.NestedSimpleRouter(router, "products", lookup="product")
review_router.register("reviews", ReviewViewSet, basename="reviews")


urlpatterns = router.urls + review_router.urls


# urlpatterns = [
#     path("products/", ProductList.as_view()),
#     path("products/<int:id>/", ProductDetail.as_view()),
#     path("collections/", CollectionList.as_view()),
#     path("collections/<int:pk>/", CollectionDetail.as_view()),
# ]


