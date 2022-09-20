from django.db import models

# Create your models here.

class Roles(models.Model):
    discord = models.TextField()
    tokenId = models.IntegerField()
    assigned = models.BooleanField(default=False)