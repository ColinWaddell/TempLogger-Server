from django.db import models


class TemperatureSensor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%d - %s" % (self.pk, self.name)


class Reading(models.Model):
    temperature_c = models.FloatField()
    sensor = models.ForeignKey(TemperatureSensor, on_delete=models.CASCADE)
    datetime = models.DateTimeField('date published')
