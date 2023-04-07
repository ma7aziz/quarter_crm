from django import forms
from . import models 

class CustomerForm(forms.ModelForm):
    class Meta :
        model = models.Customer
        fields = ['name' , 'phone_number' , 'address' , 'city' ]
        
        labels = {
            'name' : 'الاسم' ,
            'phone_number' : 'الجوال',
            'address': 'العنوان' , 
            'city' : 'المدينة'
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'required': True}),
            'phone_number': forms.TextInput(attrs={'required': True}),
            'address': forms.TextInput(attrs={'required': True}),
            'city': forms.TextInput(attrs={'required': True}),
        }