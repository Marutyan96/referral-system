# utils.py
import random
import string
from .models import User

def generate_invite_code(length=6):
    """
    Генерация случайного инвайт-кода из цифр и заглавных латинских букв.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_or_create_user(phone):
    """
    Получает пользователя по номеру телефона или создаёт нового,
    присваивая ему инвайт-код, если он ещё не задан.
    """
    user, created = User.objects.get_or_create(phone_number=phone)
    if created or not user.invite_code:
        user.invite_code = generate_invite_code()
        user.save()
    return user

def is_valid_invite_code(code):
    """
    Проверка существования инвайт-кода в базе.
    """
    return User.objects.filter(invite_code=code).exists()

def activate_invite_code(user, code):
    """
    Активирует инвайт-код у пользователя, если он ещё не активировал никакой код.
    Возвращает кортеж (успешно: bool, сообщение: str)
    """
    if user.activated_invite_code:
        return False, "Вы уже активировали инвайт-код"
    if not is_valid_invite_code(code):
        return False, "Инвайт-код не существует"
    user.activated_invite_code = code
    user.save()
    return True, "Инвайт-код успешно активирован"
