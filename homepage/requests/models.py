from django.db import models

class Request(models.Model):
    url = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
