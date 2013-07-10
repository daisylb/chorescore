from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chore (models.Model):
    name = models.CharField(max_length=256)
    score = models.PositiveSmallIntegerField()

class ChoreEvent (models.Model):
    chore = models.ForeignKey(Chore)
    user = models.ForeignKey(User)
    performed_at = models.DateTimeField(auto_now_add=True)
