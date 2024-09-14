
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from chat_app import views


router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'users', UserViewSet)


message_list = MessageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

message_detail = MessageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', rooms_view, name='rooms'),
    path('profile/', profile_view, name='profile'),
    path('users/', users_view, name='users'),
    path('users/<int:pk>/', user_detail_view, name='user-detail'),
    path('rooms/<int:pk>/', room_detail_view, name='room-detail'),

  
    # path('chatgroups/<int:chat_group_pk>/messages/', MessageViewSet.as_view({'get': 'list'}), name='message-list'),
    # path('chatgroups/<int:chat_group_pk>/messages/<int:message_pk>/', MessageViewSet.as_view({'get': 'retrieve'}), name='message-detail'),

    path('rooms/<int:chat_group_pk>/messages/<int:pk>/', message_detail, name='message-detail'),
    path('rooms/<int:chat_group_pk>/messages/', message_list, name='message-list'),
]