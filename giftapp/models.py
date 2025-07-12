from django.db import models

# Create your models here.
from django.db import models

class Gift(models.Model):
    name = models.CharField(max_length=100)
    coin = models.PositiveIntegerField()

    def __str__(self):
        return self.name
