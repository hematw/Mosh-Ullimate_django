from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .models import Gym, Amenty
from .serializers import GymSerializer, AmentySerializer
from rest_framework.serializers import ValidationError

# Create your views here.

@api_view(["GET", "POST"])
def gyms_view(req: Request):
    if req.method == "GET":
        queryset = Gym.objects.filter()
        serializer = GymSerializer(queryset, many=True)
        return Response(serializer.data)
    elif req.method == "POST":
        serializer = GymSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("ok created")
    
    
@api_view(["GET", "POST"])
def amenties_view(req: Request):
    if req.method == "GET":
        queryset = Amenty.objects.all()
        serializer = AmentySerializer(queryset, many=True)
        return Response(serializer.data)
    elif req.method == "POST":
        try:
            serializer = AmentySerializer(data=req.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "New Amenty added"})
        except ValidationError as e:
            return Response({"message": "Validation Failed"})