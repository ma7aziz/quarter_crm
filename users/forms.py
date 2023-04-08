from django.contrib.auth.forms import UserCreationForm
from . import models
from django import forms 
class CreateUserForm(UserCreationForm):

    class Meta:
        model = models.User
        install =  forms.BooleanField(label='التركيب' , required=False)
        repair = forms.BooleanField(label='الصيانة' , required=False)
        fields = ('username', 'name','password1' ,'password2' , 'phone_number', 'role',  'favourite_qouta' , 'install' , 'repair' , 'quarter') 
        labels = {
            'username': 'اسم المستخدم',
            'name': 'الاسم الكامل ',
            'phone_number': 'رقم الجوال ',
            'role': 'الوظيفة',
            'favourite_qouta': 'عدد المفضلات المسموح ',
            'password1': 'رمز المرور',
            'password2': ' تأكيد رمز المرور'
        }
        widgets = {
            'username': forms.TextInput(attrs={'required': True}),
            'name': forms.TextInput(attrs={'required': True}),
            'role': forms.Select(attrs={'required': True}),
            'password1': forms.PasswordInput(attrs={'required': True} ),
            'password2': forms.PasswordInput(attrs={'required': True}),
            'favourite_qouta' : forms.NumberInput(attrs={'required' : True }) ,

        }
        
    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop('user_role', None)
        super(CreateUserForm, self).__init__(*args, **kwargs)
        if user_role == 'install_supervisor':
            self.fields['role'].choices = [('technician', 'فني')]

