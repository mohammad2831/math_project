from django.urls import path, include
from . import views_app

app_name= 'question_app'
urlpatterns =[
   #path('', views_app.AllQuestionView.as_view(), name="all_question"),
   path('integral/<int:id_q>/', views_app.SelectQuestionIntegralView.as_view(), name='select_question_integral'),
   path('integral/<int:id_q>/<int:id_s>/', views_app.QuestionIntegralView.as_view(),name='question_integral_view'),




   path('derivative/<int:id_q>/', views_app.SelectQuestionDerivativeView.as_view(), name='select_question_derivative'),
   path('derivative/<int:id_q>/<int:id_s>/', views_app.QuestionDerivativeView.as_view(),name='question_derative_view'),


   #path('test/', views_app.test.as_view(), name="test")
   path('testacount/', views_app.testacount.as_view()),

]

