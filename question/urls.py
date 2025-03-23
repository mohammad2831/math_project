'''
from django.urls import path, include
from . import views_web

app_name= 'question'
urlpatterns =[
   path('', views_web.AllQuestionView.as_view(), name="all_question"),
   path('<int:id_q>/', views_web.SelectQuestionView.as_view(), name='select_question'),
   path('<int:id_q>/<int:id_s>/', views_web.QuestionView.as_view(),name='question_view'),


   path('test', views_web.test.as_view(), name="test")

]


'''

