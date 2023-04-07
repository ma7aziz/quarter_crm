from api.serializers import CustomerSerializer , SparePartRequestSerializer
from rest_framework import generics
from core.models import Customer
from service.models import SparePartRequest
from django.db.models import Q

class CustomerList(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    queryset  = Customer.objects.all()
    
    def get_queryset(self):
        queryset = Customer.objects.all()
        search_term = self.request.query_params.get('q', None)
        if search_term is not None:
            queryset = queryset.filter(Q(name__icontains=search_term) | Q(phone_number__icontains=search_term))
        return queryset
    
class SparePartRequestDetails(generics.RetrieveAPIView):
    serializer_class = SparePartRequestSerializer
    queryset = SparePartRequest.objects.all()
    