from django.db import models

class ProspectEmail(models.Model):
    email = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=50, blank=True)
    message = models.CharField(max_length=550, blank=True)
    link = models.CharField(max_length=50, blank=True)
    sent = models.DateTimeField(auto_now_add=True)