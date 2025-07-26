from django.urls import path
from .views import (
    RequestCodeView,
    ConfirmCodeView,
    profile_view,
    request_code_form,
    confirm_code_form,
    profile_page_view,
    index_view  # Добавьте эту импортированную view
)

app_name = 'referral'  # Добавьте пространство имен

urlpatterns = [
    # Web Interface
    path('', index_view, name='index'),  # Главная страница
    path('request-code/', request_code_form, name='request-code'),
    path('confirm-code/', confirm_code_form, name='confirm-code'),
    path('profile/', profile_page_view, name='profile'),
    
    # API Endpoints
    path('api/auth/request/', RequestCodeView.as_view(), name='api-request-code'),
    path('api/auth/confirm/', ConfirmCodeView.as_view(), name='api-confirm-code'),
    path('api/profile/', profile_view, name='api-profile'),
]