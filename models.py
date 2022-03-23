from django.db import models
from django.utils import timezone

class crop_analysis(models.Model):
    Analysis_ID_No = models.CharField(primary_key=True, max_length=255)
    Crop = models.CharField(max_length=255)
    Status = models.CharField(max_length=255)
    Disease = models.CharField(max_length=255)
    Probability = models.CharField(max_length=255)
    Date_Created = models.DateTimeField(default=timezone.now)


    class Meta:
        db_table='CropAnalysisReport'
