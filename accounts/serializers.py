from rest_framework import serializers
from .models import User




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


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)



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