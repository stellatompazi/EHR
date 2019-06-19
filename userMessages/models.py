from django.db import models
from mr.models import *
from django.contrib.auth.models import User


# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    was_read = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.username + ' - ' + self.receiver.username