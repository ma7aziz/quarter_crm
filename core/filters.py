import django_filters
from .models import Customer



class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='الأسم')
    phone_number = django_filters.CharFilter(
        lookup_expr='icontains', label='رقم الهاتف')
    city = django_filters.CharFilter(lookup_expr='icontains', label='المدينة')

    class Meta:
        model = Customer
        fields = '__all__'


