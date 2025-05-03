import random
from . models import OtpCode, User
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer, VerifyCodeSerializer, UserProfileSerializer, UserForgotpasswordSerializer, OtpResetPasswordSerializer, ResetPasswordSerializer, MyTokenObtainPairSerializer
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .permissions import IsProfileOwner
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
import jwt
from .connections import get_redis_connection
from django.core.cache import cache
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from question.models import UserProgress

import requests

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from utils import KavenegarSMS


class testOtp(APIView):
    authentication_classes = [JWTAuthentication]  # احراز هویت با توکن JWT
    permission_classes = [IsAuthenticated]
    def get(self, requsest):
        user= requsest.user
        id = user.id
        if id is None:
            print("noneeeeeeeeeee")
        return Response(user.id)
    def post(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response({"error": "شماره موبایل الزامی است."}, status=status.HTTP_400_BAD_REQUEST)

        # تولید کد OTP تصادفی ۶ رقمی
        otp_code = str(random.randint(100000, 999999))
        message = f"کد تایید شما: {otp_code}"

        sms_service = KavenegarSMS()
        response = sms_service.send_sms(phone_number, message)

        if "error" in response:
            return Response({"error": "ارسال پیامک ناموفق بود."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "کد تایید ارسال شد.", "otp": otp_code}, status=status.HTTP_200_OK)





class UserRegisterVerifyCodeView(APIView):
    def post(self, request):
        ser_data = VerifyCodeSerializer(data=request.data)
        if ser_data.is_valid():
            otp_code = ser_data.validated_data['code']
            user_data = cache.get(f'user_registration:{otp_code}')
            cache.delete(f'user_registration:{otp_code}')
            
            if not user_data:
                return Response({"error": "Invalid or expired OTP code."}, status=400)
            
            user = User.objects.create_user(
                email=user_data['email'],
                phone_number=user_data['phone_number'],
                full_name=user_data['full_name'],
                password=user_data['password']
            )
            
            OtpCode.objects.filter(phone_number=user_data['phone_number']).delete()
            
            server_host = request.get_host()  
            protocol = "https" if request.is_secure() else "http"  
            token_url = f"{protocol}://{server_host}/accounts/token/"  
            
            data = {
                'email': user.email,  
                'password': user_data['password'],
            }
            headers = {'Content-Type': 'application/json'}
            
            try:
                response = requests.post(token_url, json=data, headers=headers)
                if response.status_code == 200:
                    tokens = response.json()
                    return Response({
                        'access_token': tokens['access'],
                        'refresh_token': tokens['refresh'],
                        'status': 200
                    }, status=200)
                else:
                    return Response({
                        'error': 'Token generation failed',
                        'details': response.json(),
                    }, status=response.status_code)
            except requests.exceptions.RequestException as e:
                return Response({'error': f'Request failed: {e}'}, status=500)
        
        return Response({"error": "Invalid OTP code."}, status=400)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        
        token = super().get_token(user)
        token['id'] = user.id
        token['phone_number'] = user.phone_number
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['score'] = user.score
        token['last-question-integral'] = user.last_question_integral
        token['last-question-derivative'] = user.last_question_derivative
        
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


#test clss for test authentication and authrization
class Test(APIView):
    authentication_classes = [JWTAuthentication]  # احراز هویت با توکن JWT
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        print("hiiiiiiiiiii")
        return Response({'hi':'test is ok'})









#reset and change the password

class ResetPasswordView(APIView):
    authentication_classes = [TokenAuthentication] 

    def put(self, request):
        user_session = request.session.get('forgot_password_info')
        if not user_session:
            return Response({'message': 'Session expired or invalid.'}, status=400)

        try:
            user = User.objects.get(phone_number=user_session['phone_number'])
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=404)

        ser_data = ResetPasswordSerializer(data=request.data)
        if ser_data.is_valid():
            new_password = ser_data.validated_data['new_password']
            
            user.set_password(new_password)
            user.save()  

            return Response({'message': 'Password updated successfully.'}, status=200)
        return Response(ser_data.errors, status=400)



#verify otp code for forgot password function
class OtpResetPasswordView(APIView):
     def post(self, request):
        user_session=request.session['forgot_password_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        user = User.objects.get(phone_number=user_session['phone_number'] )


        ser_data = OtpResetPasswordSerializer(data=request.data)
        if ser_data.is_valid():
            code = ser_data.validated_data['code']
            try:
                if int(code) == code_instance.code:  
                    token, created = Token.objects.get_or_create(user=user)
                    print(token.key)
                    return Response({'status': 201, 'message': 'Code verified successfully.','token': token.key,})
                else:
                    return Response({'status': 407, 'message': 'Invalid code.'}, status=400)
            except OtpCode.DoesNotExist:
                return Response({'status': 407, 'message': 'Phone number not found.'}, status=404)
        return Response({'status': 407, 'message': 'Invalid data.'}, status=400)



# send otp code for forgot password function
class UserForgotpasswordView(APIView):
    def post(self, request):
        ser_data = UserForgotpasswordSerializer(data = request.data)
        if ser_data.is_valid():          
            phone = ser_data.validated_data['phone']
            user = get_object_or_404(User, phone_number=phone)


            random_code = random.randint(1000, 9999)


            request.session['forgot_password_info'] = {
                'phone_number' : ser_data.validated_data['phone'],
                'code':random_code
            }

            OtpCode.objects.create(phone_number = ser_data.validated_data['phone'], code=random_code)
            return Response({'code':random_code,'status':201} )

        return Response(ser_data.errors, status=400)






   
class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        #user = User.objects.get(email=request.user.email)
        user = request.user 
        ser_data = UserProfileSerializer(user)
        return Response(ser_data.data, status=200)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class UserLoginView(APIView):
    def post(self, request):
        ser_data = UserLoginSerializer(data=request.data)
        print("heloo")

        if ser_data.is_valid():
            phone_number = ser_data.validated_data['phone_number']
            password = ser_data.validated_data['password']

            user = get_object_or_404(User,phone_number=phone_number)
            if user.check_password(password):

                server_host = request.get_host()  
                protocol = "https" if request.is_secure() else "http"  
                token_url = f"{protocol}://{server_host}/accounts/token/"  
            
           
                data = {
                    'email': user.email,  
                    'password': password,
                }
                headers = {'Content-Type': 'application/json'}
            
                try:
                    response = requests.post(token_url, json=data, headers=headers)
                    if response.status_code == 200:
                        tokens = response.json()
                        return Response({
                            'access_token': tokens['access'],
                            'refresh_token': tokens['refresh'],
                            'status': 200
                        }, status=200)
                    else:
                        return Response({
                            'error': 'Token generation failed',
                            'details': response.json(),
                        }, status=response.status_code)
                except requests.exceptions.RequestException as e:
                    return Response({'error': f'Request failed: {e}'}, status=500)


            else:
                return Response({"error": "Invalid phone number or password"}, status=400)
        return Response({"error": "Invalid input data "}, status=400)


        

class UserRegisterView(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            random_code = random.randint(1000, 9999)
       #     send_otp_code(ser_data.validated_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number = ser_data.validated_data['phone_number'], code=random_code)
            user_data = {
                'email' : ser_data.validated_data['email'],
                'phone_number' : ser_data.validated_data['phone_number'],
                'full_name' : ser_data.validated_data['full_name'],
                'password' : ser_data.validated_data['password'],
                'otp': random_code
            }

            cache.set(f'user_registration:{random_code}', user_data, timeout=920)
            return Response({"code":random_code,}, status=200)
        return Response({"error": "Invalid data."}, status=400)




class UserLogoutView(APIView):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]

    def post(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return Response({"detail": "Authorization header missing."}, status=400)

        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return Response({"detail": "Invalid authorization header."}, status=400)

        access_token = parts[1]

        try:
            refresh_token = RefreshToken(access_token)
        except TokenError as e:
            return Response({"detail": f"Invalid token: {str(e)}"}, status=400)

        redis = get_redis_connection('default')
        redis.setex(f"blacklisted_{access_token}", 3600, access_token)  # ذخیره توکن به مدت 1 ساعت

        return Response({"detail": "Successfully logged out."}, status=200)
    




