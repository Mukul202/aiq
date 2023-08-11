from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Q
from .models import PowerPlantModel, StateModel
from .serializers import PowerPlantSerializer, StateSerializer


class NetGenerationFilterBackend(BaseFilterBackend):
    def filter_queryset(self,request,queryset,view):
        min_net_generation = request.query_params.get('min_net_generation')
        max_net_generation = request.query_params.get('max_net_generation')
        
        if min_net_generation is not None and float(min_net_generation)>=0:
            queryset=queryset.filter(annual_net_generation__gte=min_net_generation)
        
        if max_net_generation is not None and float(max_net_generation)>=0:
            queryset=queryset.filter(annual_net_generation__lte=max_net_generation)
            
        return queryset
    
class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit=10
    max_limit=20000
    
    def get_limit(self, request):
        # Get the custom limit from query parameters, if provided
        limit = super().get_limit(request)
        custom_limit = request.query_params.get('n')
        
        if custom_limit:
            try:
                custom_limit = int(custom_limit)
                if 1 <= custom_limit <= self.max_limit:
                    limit = custom_limit
            except ValueError:
                pass
        
        return limit
    
class CustomSearchFilter(BaseFilterBackend):
    def filter_queryset(self,request,queryset,view):
        search_query=request.query_params.get('state')
        if(search_query):
            queryset=queryset.filter(
                Q(plant_state__icontains=search_query)
            )
        return queryset
    
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self,request,view):
        if request.method in ['GET','HEAD','OPTIONS']:
            return True
        return request.user and request.user.is_staff

class PowerPlantsView(generics.ListCreateAPIView):
    queryset=PowerPlantModel.objects.all().order_by('-annual_net_generation')
    serializer_class=PowerPlantSerializer
    pagination_class=CustomLimitOffsetPagination
    filter_backends=[NetGenerationFilterBackend,CustomSearchFilter]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    permission_classes=[IsAdminOrReadOnly]
    authentication_classses=[JWTAuthentication]
    
    @method_decorator(cache_page(60*5))
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Calculate and add 'percentage' field to each item in the response data
        data = response.data
        
        for item in data['results']:
            
            annual_net_generation = item['annual_net_generation']
            state_id = item['plant_state']
            state_annual_net_generation = StateModel.objects.get(state_name=state_id).state_annual_net_generation
            
            # Calculate the percentage and round it to two decimal points
            if state_annual_net_generation != 0:
                percentage = round((annual_net_generation / state_annual_net_generation) * 100, 2)
            else:
                percentage = 0.0  # Handle division by zero if needed

            # Add the calculated percentage to the item dictionary
            item['percentage'] = percentage
        
        return Response(data)

class SinglePowerPlantView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset=PowerPlantModel.objects.all()
    serializer_class=PowerPlantSerializer
    permission_classes=[IsAdminOrReadOnly]
    authentication_classes=[JWTAuthentication]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    
    @method_decorator(cache_page(60*5))
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        
        # Calculate and add 'percentage' field to the item in the response data
        item = response.data
        
        annual_net_generation = item['annual_net_generation']
        state_id = item['plant_state']
        state_annual_net_generation = StateModel.objects.get(state_name=state_id).state_annual_net_generation
        
        # Calculate the percentage and round it to two decimal points
        if state_annual_net_generation != 0:
            percentage = round((annual_net_generation / state_annual_net_generation) * 100, 2)
        else:
            percentage = 0.0  # Handle division by zero if needed

        # Add the calculated percentage to the item dictionary
        item['percentage'] = percentage
        
        return Response(item)
    
    
class StatesView(generics.ListCreateAPIView):
    queryset=StateModel.objects.all()
    serializer=StateSerializer
    
class SingleStateView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset=StateModel.objects.all()
    serializer=StateSerializer
    

    