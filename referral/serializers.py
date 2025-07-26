from rest_framework import serializers
from .models import User

class PhoneInputSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class CodeInputSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

class InviteCodeInputSerializer(serializers.Serializer):
    invite_code = serializers.CharField()
