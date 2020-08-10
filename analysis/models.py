from datetime import timezone

from django.db import models

class Red(models.Model):
    nicotine_mean = models.CharField(max_length=255)
    nicotine_sd = models.CharField(max_length=255)
    nicotine_cp = models.CharField(max_length=255)
    flavoring_mean = models.CharField(max_length=255)
    flavoring_sd = models.CharField(max_length=255)
    flavoring_cp = models.CharField(max_length=255)
    blending_mean = models.CharField(max_length=255)
    blending_sd = models.CharField(max_length=255)
    blending_cp = models.CharField(max_length=255)
    sugar_mean = models.CharField(max_length=255)
    sugar_sd = models.CharField(max_length=255)
    sugar_cp = models.CharField(max_length=255)
    rsugar_mean = models.CharField(max_length=255)
    rsugar_sd = models.CharField(max_length=255)
    rsugar_cp = models.CharField(max_length=255)
    chlorine_mean = models.CharField(max_length=255)
    chlorine_sd = models.CharField(max_length=255)
    chlorine_cp = models.CharField(max_length=255)
    potassium_mean = models.CharField(max_length=255)
    potassium_sd = models.CharField(max_length=255)
    potassium_cp = models.CharField(max_length=255)
    nitrogen_mean = models.CharField(max_length=255)
    nitrogen_sd = models.CharField(max_length=255)
    nitrogen_cp = models.CharField(max_length=255)
    def __str__(self):
        return "%s:%s:%s:%s:%s:%s:%s"%(self.nicotine_mean,self.nicotine_sd,self.nicotine_cp,self.flavoring_mean,self.flavoring_sd,self.flavoring_cp,self.blending_mean)

    class Meta:
        db_table = "red"