from django.db import models
from authentication.models import Account

class Project(models.Model):
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, db_constraint=False)
    name = models.CharField(max_length=100, unique=True)
    at_create = models.DateTimeField()
    at_update = models.DateTimeField()
    
    class Meta:
        db_table = "projects"
        

class Fly(models.Model):
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, db_constraint=False)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, db_constraint=False)
    name = models.CharField(max_length=100)
    at_create = models.DateTimeField()
    at_fly = models.DateField(blank=True, null=True)
    robot_type = models.CharField(null=True, max_length=100)
    camera_type = models.CharField(null=True, max_length=100)
    commentary = models.TextField(null=True)
    images_coords = models.TextField()
    
    class Meta:
        db_table = "flying"


class ObservationObjectChronology(models.Model):
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    at_create = models.DateTimeField()
    at_update = models.DateTimeField()
    name = models.CharField(max_length=100)
    coordinate = models.CharField(max_length=100)
    commentary = models.TextField()
    
    class Meta:
        db_table="observation_object_chronology"


class FlyImage(models.Model):
    fly = models.ForeignKey(Fly, on_delete=models.SET_NULL, null=True)
    coordinate = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    
    class Meta:
        db_table="fly_image"
        

class ObservationObject(models.Model):
    chronology = models.ForeignKey(ObservationObjectChronology, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    at_create = models.DateTimeField()
    image = models.ForeignKey(FlyImage, on_delete=models.CASCADE, null=True)
    image_box = models.CharField(max_length=100)
    commentary = models.TextField()
    
    class Meta:
        db_table="observation_object"