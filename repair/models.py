from service.models import Service_request
from accounts.models import User
from django.db import models


class SparePartRequst(models.Model):

    """
    Spare parts request for repair request
    """
    STATUS = [
        ("open", 'open'),
        ("closed", 'closed')
    ]
    service_request = models.ForeignKey(Service_request , on_delete=models.CASCADE)
    part_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(max_length=500 , blank=True , null = True)
    status = models.CharField(max_length=10 , choices=STATUS , default="open")
    company = models.ForeignKey(User , on_delete=models.SET_NULL , null = True ,  blank = True )
    files = models.ManyToManyField("SparePartsRequestFile" , blank=True , related_name="spare_part_file")
    created_by = models.ForeignKey(User ,on_delete=models.SET_NULL , null = True , related_name="request_creator")

    def __str__(self):
        return f"{self.part_name} for {self.service_request}"




class SparePartsRequestFile(models.Model):
    request = models.ForeignKey(SparePartRequst , on_delete=models.CASCADE)
    file = models.FileField(upload_to='service/files/spare_parts_requests')

    def __str__(self):
        return f'Spare part request for #{self.request.service_request}'