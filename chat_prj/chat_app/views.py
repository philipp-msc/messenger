# from django.shortcuts import render, redirect
# from .models import *


# def CreateRoom(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         room = request.POST['room']

#         try:
#             get_room = Room.objects.get(room_name=room)
#         except Room.DoesNotExist:
#             new_room = Room(room_name=room)
#             new_room.save()
#         return redirect('room', room_name=room, username=username)
#     return render(request,'index.html')

# def MessageView(request, room_name, username):
#     get_room = Room.objects.get(room_name=room_name)
#     get_messages = Message.objects.filter(room=get_room)

#     context = {
#         'messages': get_messages,
#         'user': username,
#         'room_name': room_name,
#     }
#     return render(request, 'message.html', context)

# from rest_framework import viewsets
# from .models import Room, Message
# from .serializers import RoomSerializer, MessageSerializer #, UserSerializer


# class RoomViewSet(viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer


# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

from rest_framework import viewsets
from .models import *
from .serializers import RoomSerializer, MessageSerializer, UserSerializer
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.members.add(self.request.user)
        instance.save()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all()

        chat_group_pk = self.kwargs.get('chat_group_pk')
        if chat_group_pk is not None:
            queryset = queryset.filter(room_id=chat_group_pk)
        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, room_id=self.kwargs['chat_group_pk'])


def message_list(request, chat_group_pk):
    messages = Message.objects.filter(room_id=chat_group_pk)
    return render(request, 'message_list.html', {'messages': messages})

@login_required
def home_view(request):
    return render(request, 'index.html')

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required
def users_view(request):
    users = User.objects.all()
    for user in users:
        print(reverse('user-detail', kwargs={'pk': user.pk}))
    return render(request, 'users.html', {'users': users})


@login_required
def rooms_view(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})

@login_required
def user_detail_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

@login_required
def room_detail_view(request, pk):
    rooms = get_object_or_404(Room, pk=pk)
    return render(request, 'room_detail.html', {'room': rooms})




