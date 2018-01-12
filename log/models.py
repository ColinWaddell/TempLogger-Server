from django.db import models


class TemperatureSensor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%d - %s" % (self.pk, self.name)

    def get_temperature(self):
        try:
            recent = Reading.objects.filter(sensor=self).order_by('-id')[0].temperature_c
        except (IndexError, AttributeError):
            recent = -1.0
        finally:
            return recent


class Reading(models.Model):
    temperature_c = models.FloatField()
    sensor = models.ForeignKey(TemperatureSensor, on_delete=models.CASCADE)
    datetime = models.DateTimeField('date published')
