from django.shortcuts import render, redirect
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib import messages
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from.models import Room
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


@login_required
def home_view(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '!نام کاربری یا رمز عبور اشتباه است')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, '!رمز عبور مطابقت ندارد')
        elif User.objects.filter(username=username).exists():
            messages.error(request,'!این کاربر قبلا ثبت نام شده است')
        elif User.objects.filter(email=email).exists():
            messages.error(request, '!ایمیل قبلاً ثبت‌نام شده است')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('home')

    return render(request, 'register.html')


def mainview(request):
    rooms = Room.objects.all()
    messages = Message.objects.all()
    return render(request, 'chat.html', {'rooms': rooms, 'messages': messages})

def create_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        
        
        if Room.objects.filter(name=room_name).exists():
            messages.error(request, "این روم قبلاً وجود دارد. لطفاً نام دیگری وارد کنید")
        else:
            if room_name:
                Room.objects.create(name=room_name, created_by=request.user)
                messages.success(request, "روم با موفقیت ایجاد شد")
    
    return redirect('home')





class Roomview(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = Roomserializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class Messageview(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = Messageserializer
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['get'], url_path='by-room/(?P<room_id>[^/.]+)')
    def messages_by_room(self, request, room_id=None):
        messages = Message.objects.filter(room_id=room_id)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    

   
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_message(self, request, pk=None):
        message = get_object_or_404(Message, pk=pk)
    
        if message.sender == request.user:
            message.delete()
            return Response({'status': 'success'}, status=200)
        else:
            return Response({'error': 'شما مجاز به حذف این پیام نیستید.'}, status=403)

    



