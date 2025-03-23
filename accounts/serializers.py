from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from question .models import UserProgress
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate




from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # اضافه کردن فیلدهای دلخواه به توکن
        token['phone_number'] = user.phone_number
        token['full_name'] = user.full_name
        token['email'] = user.email
        # می‌توانید فیلدهای دیگر را هم اضافه کنید

        return token

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)























class ResetPasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField(write_only=True)

   
    






class OtpResetPasswordSerializer(serializers.Serializer):
    code = serializers.IntegerField()







class UserForgotpasswordSerializer(serializers.Serializer):
   
    phone = serializers.CharField(max_length=11)
    def validate_phone_number(self, value):
        if len(value) < 10 or not value.isdigit():
            raise serializers.ValidationError("Please enter a valid phone number.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone_number', 'profile_img']






class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    

 

class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value
    
    def validate_full_name(self, value):
        if User.objects.filter(full_name=value).exists():
            raise serializers.ValidationError("This name is already registered.")
        return value
    
    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value