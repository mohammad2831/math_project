from django.urls import path
from . import views

app_name= 'accounts'
urlpatterns =[
  
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name= 'user_register_verify_code'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'), 


    path('reset_password/',views.ResetPasswordView.as_view(), name='reset_password'),
    path('otp_reset_password/', views.OtpResetPasswordView.as_view(), name='otp_reset_password'),
    path('forgot_password/', views.UserForgotpasswordView.as_view(), name='forgot_password')




  
    
]