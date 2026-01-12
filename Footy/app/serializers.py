from rest_framework.serializers import ModelSerializer
from .models import Gym

class GymSerializer(ModelSerializer):
    class Meta: 
        model = Gym
        fields = ["id", "name", "description", "owner_id", "address", "latitude", "longitude", "opening_time", "closing_time"]