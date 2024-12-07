from .views import logout_view, login_view, register_view, home_view,mainview
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Roomview, Messageview,create_room


router = DefaultRouter()
router.register(r'rooms', Roomview, basename='room')
router.register(r'messages', Messageview, basename='message')


urlpatterns = [
    
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('chat/', mainview, name='chat'),
    path('api/messages/by-room/<int:room_id>/', Messageview.as_view({'get': 'messages_by_room'}), name='messages_by_room'),
    path('create-room/', create_room, name='create_room'),
    

    path('api/', include(router.urls)),
    ]
