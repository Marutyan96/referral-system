# views.py 
import time
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import (
    PhoneInputSerializer,
    CodeInputSerializer,
    InviteCodeInputSerializer
)
from .utils import get_or_create_user
import random

class RequestCodeView(APIView):
    def post(self, request):
        serializer = PhoneInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']
        code = f"{random.randint(1000, 9999)}"
        request.session['auth_code'] = code
        request.session['auth_phone'] = phone
        # В реальном приложении здесь должен быть вызов сервиса отправки SMS
        time.sleep(2)
        return Response({"status": "success", "message": "Код отправлен"})

class ConfirmCodeView(APIView):
    def post(self, request):
        serializer = CodeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        if phone != request.session.get('auth_phone'):
            return Response({"error": "Неверный номер телефона"}, status=400)
        if request.session.get('auth_code') != code:
            return Response({"error": "Неверный код"}, status=400)

        user = get_or_create_user(phone)
        request.session['user_phone'] = phone
        request.session.pop('auth_code', None)
        request.session.pop('auth_phone', None)
        return Response({
            "status": "success",
            "invite_code": user.invite_code,
            "phone_number": user.phone_number
        })

@api_view(['GET', 'POST'])
def profile_view(request):
    phone = request.query_params.get("phone_number") if request.method == 'GET' else request.data.get("phone_number")
    if not phone:
        return Response({"error": "Не указан номер телефона"}, status=400)

    user = User.objects.filter(phone_number=phone).first()
    if not user:
        return Response({"error": "Пользователь не найден"}, status=404)

    if request.method == 'GET':
        referrals = User.objects.filter(activated_invite_code=user.invite_code).values_list('phone_number', flat=True)
        return Response({
            "phone_number": user.phone_number,
            "invite_code": user.invite_code,
            "activated_invite_code": user.activated_invite_code,
            "referrals": list(referrals)
        })

    serializer = InviteCodeInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data['invite_code']

    if user.activated_invite_code:
        return Response({"error": "Вы уже активировали инвайт-код"}, status=400)
    if not User.objects.filter(invite_code=code).exists():
        return Response({"error": "Инвайт-код не существует"}, status=404)

    user.activated_invite_code = code
    user.save()
    return Response({"status": "success", "message": "Инвайт-код успешно активирован"})

@csrf_exempt
def index_view(request):
    return render(request, 'index.html')

@csrf_exempt
def request_code_form(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        if not phone:
            return render(request, 'index.html', {'error': 'Введите номер телефона'})
        code = str(random.randint(1000, 9999))
        request.session['auth_code'] = code
        request.session['auth_phone'] = phone
        request.session.modified = True  # Важно для сохранения сессии
        time.sleep(2)
        return render(request, 'index.html', {
            'message': f'Код отправлен на {phone}',
            'show_confirm_form': True,
            'phone': phone
        })
    return redirect('/')

@csrf_exempt
def confirm_code_form(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        code = request.POST.get('code')
        if not phone or not code:
            return render(request, 'index.html', {'error': 'Заполните все поля'})
        if phone != request.session.get('auth_phone'):
            return render(request, 'index.html', {'error': 'Неверный номер телефона'})
        if request.session.get('auth_code') != code:
            return render(request, 'index.html', {
                'error': 'Неверный код',
                'show_confirm_form': True,
                'phone': phone
            })
        user = get_or_create_user(phone)
        request.session['user_phone'] = phone
        request.session.pop('auth_code', None)
        request.session.pop('auth_phone', None)
        return render(request, 'index.html', {
            'message': f'Добро пожаловать! Ваш инвайт-код: {user.invite_code}',
            'show_profile': True,
            'user': user
        })
    return redirect('/')

@csrf_exempt
def profile_page_view(request):
    phone = request.session.get('user_phone')
    if not phone:
        return redirect('/')
    
    user = User.objects.filter(phone_number=phone).first()
    if not user:
        return render(request, 'index.html', {'error': 'Пользователь не найден'})

    if request.method == 'POST':
        code = request.POST.get('invite_code')
        if not code:
            return render(request, 'index.html', {'error': 'Введите инвайт-код', 'show_profile': True, 'user': user})
        if user.activated_invite_code:
            return render(request, 'index.html', {'error': 'Вы уже активировали инвайт-код', 'show_profile': True, 'user': user})
        if not User.objects.filter(invite_code=code).exists():
            return render(request, 'index.html', {'error': 'Инвайт-код не существует', 'show_profile': True, 'user': user})
        
        user.activated_invite_code = code
        user.save()
        return render(request, 'index.html', {
            'message': 'Инвайт-код успешно активирован!',
            'show_profile': True,
            'user': user
        })

    referrals = User.objects.filter(activated_invite_code=user.invite_code)
    return render(request, 'index.html', {
        'show_profile': True,
        'user': user,
        'referrals': referrals
    })