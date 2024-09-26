from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return self.name
