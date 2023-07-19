from django.db import models

# Create your models here.
class TotalForcast(models.Model):
    time = models.DateTimeField()
    city = models.CharField(max_length=100)
    latitude = models.FloatField(default="")
    longitude = models.FloatField(default="")
    temperature = models.FloatField(default="")
    feels_like = models.CharField(max_length=30, default="", null=True)  # Allow null values
    temp_min = models.FloatField(default="")
    temp_max = models.FloatField(default="")
    pressure = models.FloatField(default="")
    humidity = models.FloatField(default="")
    visibility = models.IntegerField(default="")
    weather_description = models.CharField(max_length=100, default="")
    weather_icon = models.CharField(max_length=10)