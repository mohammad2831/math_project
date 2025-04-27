from django.urls import path, include
from . import views_app

app_name= 'question_app'
urlpatterns =[
   path('', views_app.AllQuestionView.as_view(), name="all_question"),
   path('<int:id_q>/', views_app.SelectQuestionView.as_view(), name='select_question'),
   path('<int:id_q>/<int:id_s>/', views_app.QuestionView.as_view(),name='question_view'),


   #path('test/', views_app.test.as_view(), name="test")
   path('test/', views_app.test_ws, name='test-ws'),

]

