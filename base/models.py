from django.db import models

# Create your models here.
<<<<<<< Updated upstream
=======

class Files(models.Model):
    name = models.CharField(max_length=30)
    image = models.TextField()
         
def __unicode__(self):
    return self.name


class Shape(models.Model):
    points = models.TextField()
    scale = models.FloatField()
>>>>>>> Stashed changes
