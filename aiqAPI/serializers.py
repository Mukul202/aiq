from rest_framework import serializers

from .models import PowerPlantModel, StateModel

class PowerPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model=PowerPlantModel
        fields=['id','plant_name','plant_state','annual_net_generation','longitude','latitude']
        
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model=StateModel
        fields=['id','state_name','state_annual_net_generation']
    