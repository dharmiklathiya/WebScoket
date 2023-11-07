from django.db import models

# Create your models here.

class Chat(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    group=models.ForeignKey('Group',on_delete=models.CASCADE)
    objects = models.Manager

class Group(models.Model):
    name = models.CharField(max_length=255)
    objects = models.Manager

    def __str__(self):
        return self.name

