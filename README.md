# Referral System API

Простая реферальная система с авторизацией по номеру телефона и инвайт-кодами.

## 🚀 Демо

**API доступен по адресу:**  
👉 [http://83.222.19.174:8080/](http://83.222.19.174:8080/)

🧪 Тестирование
Импортируйте файл Referral System.postman_collection.json в Postman.
Коллекция включает все необходимые запросы с переменными:

base_url

phone_number

auth_code

auth_token

invite_code

🛠️ Стек технологий
Python

Django

Django REST Framework

PostgreSQL

Docker + Docker Compose

## 📌 Функциональность

- Авторизация по номеру телефона (с имитацией отправки 4-значного кода и задержкой).
- Генерация уникального 6-значного инвайт-кода при первой авторизации.
- Возможность ввести чужой инвайт-код (один раз).
- Получение профиля пользователя с:
  - Номером телефона
  - Собственным инвайт-кодом
  - Использованным чужим инвайт-кодом
  - Списком пользователей, которые ввели его код

## ⚙️ Локальный запуск

```bash
git clone https://github.com/Marutyan96/referral-system.git
cd referral-system
docker-compose down -v && docker-compose up --build




