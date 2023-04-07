from django.forms import ModelForm
from .models import QuarterProject

class QuarterProjectForm(ModelForm):
    class Meta:
        model = QuarterProject
        fields = ['name', 'phone_number', 'address']
        labels = {
            'name': 'اسم العميل',
            'phone_number': 'الجوال',
            'address': 'الموقع',
        }