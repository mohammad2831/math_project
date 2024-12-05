from django.urls import path, include
from . import views

app_name= 'question'
urlpatterns =[
   path('', views.AllQuestionView.as_view(), name="all_question"),
   path('<int:id_q>/', views.SelectQuestionView.as_view(), name='select_question'),
   path('<int:id_q>/<int:id_s>/', views.QuestionView.as_view(),name='question_view')

]




