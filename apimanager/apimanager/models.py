from django.db import models

# Create your ConectNE models here.
class ConnectNE(models.Model):
    handle = models.CharField(max_length=100, default=None)
    username = models.CharField(max_length=100, default = "temp")
    password = models.CharField(max_length=100, default="root")
    hostname = models.CharField(max_length=100, default=None)
    port_number = models.IntegerField(default=22)
    interface = models.CharField(max_length=50, default="CLI")

# Create your DisconnectNE models here.
class DiconnectNE(models.Model):
    handle = models.CharField(max_length=100, default='', blank=True)
    username = models.CharField(max_length=100, default = "temp")
    password = models.CharField(max_length=100, default="root")
    hostname = models.CharField(max_length=100, default=None)
    port_number = models.IntegerField(default=22)
    interface = models.CharField(max_length=50, default="CLI")

# Create your SendRCV models here.
class SendRCV(models.Model):
    handle = models.CharField(max_length=100, null=False, default="CLI")
    command = models.CharField(max_length=100, null=True, blank=True)  # Change the default and allow null/blank
    timeout = models.IntegerField(default=20)
    confirmI = models.BooleanField(default=False)
    step = models.BooleanField(default=False)
    match = models.CharField(max_length=100, null=True, blank=True)
    poll = models.BooleanField(default=False)
    stash = models.CharField(max_length=100, null=True, blank=True)
    mode = models.CharField(max_length=10, default="ssh")
    sendOnly = models.BooleanField(default=False)
    rcvOnly = models.BooleanField(default=False)