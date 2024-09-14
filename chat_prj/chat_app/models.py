from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Room(models.Model):
    room_name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='chat_groups')

    def __str__(self):
        return self.room_name
    
class Profile(User):

    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])



class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

