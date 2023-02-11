from django.db import models
from django.db.models.expressions import RawSQL
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):
    username = models.CharField(verbose_name=_("Username"),max_length=50,unique=True)
    email = models.EmailField(verbose_name=_("email"),blank=True,null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "Users"
        verbose_name_plural = "Users"
        default_permissions = ()
        permissions = ()
        
        
class Business(models.Model):
    business_name = models.CharField(verbose_name=_("Business Name"),max_length=50)
    place_name = models.CharField(verbose_name=_("Place Name"),max_length=70)
    latitude = models.DecimalField(max_digits=30,null=True,decimal_places=25,verbose_name=_("Latitude"))
    longitude = models.DecimalField(max_digits=30,null=True,decimal_places=25,verbose_name=_("Longitude"))

    def __str__(self):
        return self.business_name
    
    @staticmethod
    def nearby(latitude, longitude, distance_range):
        queryset = Business.objects.all()
        if not (latitude and longitude and distance_range):
            return queryset.none()
        
        latitude       = float(latitude)
        longitude      = float(longitude)
        distance_range = float(distance_range)
        gcd_formula = """6371 * acos(least(greatest(
        cos(radians(%s)) * cos(radians(latitude)) 
        * cos(radians(longitude) - radians(%s)) + 
        sin(radians(%s)) * sin(radians(latitude)) 
        , -1), 1))"""
        distance_raw_sql = RawSQL(
            gcd_formula,
            (latitude, longitude, latitude)
        )
        qs = \
        queryset.annotate(distance=distance_raw_sql).\
        filter(distance__lte=distance_range).order_by('distance')
        return qs

    class Meta:
        db_table = "Business"
        verbose_name_plural = "Business"
        default_permissions = ()
        permissions = ()
        
   