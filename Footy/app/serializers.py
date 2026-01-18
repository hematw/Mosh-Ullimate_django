from rest_framework.serializers import ModelSerializer
from .models import Gym, Amenty

class GymSerializer(ModelSerializer):
    class Meta: 
        model = Gym
        fields = ["id", "name", "description", "owner_id", "address", "latitude", "longitude", "opening_time", "closing_time"]
        
        
class AmentySerializer(ModelSerializer):
    class Meta:
        model = Amenty
        fields = ["id", "name", "icon"]