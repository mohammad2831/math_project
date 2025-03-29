from django.urls import path
from . import views


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MyTokenObtainPairView



app_name= 'accounts'
urlpatterns =[
  
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name= 'user_register_verify_code'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'), 


    path('reset_password/',views.ResetPasswordView.as_view(), name='reset_password'),
    path('otp_reset_password/', views.OtpResetPasswordView.as_view(), name='otp_reset_password'),
    path('forgot_password/', views.UserForgotpasswordView.as_view(), name='forgot_password'),


    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   path('test/', views.Test.as_view(), name='test_jwt'),

   path('testotp/', views.testOtp.as_view(), name='testotp'),
    
]