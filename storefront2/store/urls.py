from django.urls import path
from .views import ProductViewSet, CollectionViewSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("products", ProductViewSet)
router.register("collections", CollectionViewSet)

urlpatterns = router.urls


# urlpatterns = [
#     path("products/", ProductList.as_view()),
#     path("products/<int:id>/", ProductDetail.as_view()),
#     path("collections/", CollectionList.as_view()),
#     path("collections/<int:pk>/", CollectionDetail.as_view()),
# ]


