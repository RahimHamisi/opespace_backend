
import uuid
from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.db import models
from utils.randomized_id import generate_reference_id



# Create your models here.
class OpenSpace(models.Model):
    openspace_id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name=models.CharField(max_length=50,blank=False,null=False)
    latitude = models.FloatField(blank=True, null=True)
    longtude = models.FloatField(blank=True, null=True)
    easting = models.FloatField(blank=True, null=True)  
    northing = models.FloatField(blank=True, null=True)  
    utm_zone = models.CharField(max_length=10, blank=True, null=True) 
    description=models.CharField(max_length=100,null=True,blank=True)
    area_size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    region = models.CharField(max_length=100, default="Dar es Salaam")  
    district = models.CharField(max_length=100, default="Kinondoni")  
    ward = models.CharField(max_length=100, blank=True, null=True)     
    street = models.CharField(max_length=100, blank=True, null=True) 
    managed_by = models.CharField(max_length=100, blank=True, null=True)  
    contact_info = models.CharField(max_length=100, blank=True, null=True) 
    is_active = models.BooleanField(default=True)  


    def __str__(self):
        return f" self.name "



class Report(models.Model):
    CATEGORY_CHOICES = [
        ('vandalism', 'Vandalism'),
        ('littering', 'Littering'),
        ('unauthorized_activity', 'Unauthorized Activity'),
        ('illegal_dumping', 'Illegal Dumping'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_investigation', 'Under Investigation'),
        ('resolved', 'Resolved'),
    ]
    report_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    reference_id=models.CharField(max_length=8,editable=False,default=generate_reference_id,unique=True)
    open_space=models.ForeignKey(OpenSpace,on_delete=models.CASCADE,related_name='open_space')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL,null = True,blank = True,related_name = 'user_reports') 
    description = models.TextField() 
    category = models.CharField(max_length = 50,choices = CATEGORY_CHOICES) 
    date_reported = models.DateTimeField(auto_now_add = True) 
    status = models.CharField(max_length = 20,choices = STATUS_CHOICES,default = 'pending')
    assigned_to = models.CharField(max_length = 100,blank = True,null = True) 
    resolution_date = models.DateField(blank = True, null = True) 
    is_active=models.BooleanField(default=True)



    def __str__(self): 
        return f"Report {self.reference_id} - Ref: {self.reference_id} - {self.category} - {self.status}"
