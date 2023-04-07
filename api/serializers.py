from core.models import Customer
from rest_framework import serializers 
from service.models import SparePartRequest , Service
from users.models import User

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Customer
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , ] 
        
class ServiceSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    company= UserSerializer()
    class Meta:
        model = Service
        fields = '__all__'
        
                    
class SparePartRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    recievied_by = UserSerializer()
    service = ServiceSerializer()
    
    class Meta:
        model = SparePartRequest
        fields = '__all__'
        
