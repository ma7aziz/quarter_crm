from django.forms import ModelForm
from .models import Repair_request


class RepairRequestForm(ModelForm):
    class Meta:
        model = Repair_request
        exclude = ('status', )
