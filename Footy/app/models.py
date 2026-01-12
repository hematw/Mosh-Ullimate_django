from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Gym(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner_id = models.ForeignKey(User, models.RESTRICT)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    
    
    
class Court(models.Model):
    court_types = (
        ("futsal", "Futsal"),
        ("football", "Football"),
    )
    
    surface_types = (
        ("grass", "Grass"),
        ("turf",  "Turf"),
        ("indoor", "Indoor"),
    )
    
    id = models.UUIDField(auto_created=True, primary_key=True)
    gym_id = models.ForeignKey(to=Gym, on_delete=models.CASCADE)
    name =  models.CharField(max_length=255)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    player_capacity = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=16, choices=court_types)
    surface = models.CharField(max_length=16, choices=surface_types)
    is_active =  models.BooleanField(default=True)
    
    
    
class Booking(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True)
    court_id = models.ForeignKey(Court, on_delete=models.RESTRICT)
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    
class Amenty(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=255)
    icon = models.URLField()
