from django.db import models
from django.contrib.gis.db import models as geomodels

# Create your models here.
class PowerPlantModel(models.Model):
    plant_name=models.CharField(max_length=100)
    plant_state = models.CharField(max_length=2)
    annual_net_generation = models.IntegerField()
    longitude = models.FloatField()
    latitude= models.FloatField()
    
    def __str__(self) -> str:
        return self.plant_name
    
    
class StateModel(models.Model):
    state_name=models.CharField(max_length=2)
    state_annual_net_generation=models.IntegerField()
    
    def __str__(self) -> str:
        return self.state_name
    
