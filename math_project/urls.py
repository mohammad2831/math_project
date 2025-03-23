
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('web', include('web.urls', namespace='web')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('question-app/', include('question.urls_app', namespace='question_app')),
    path('question-web/', include('question.urls_web', namespace='question_web')),
   # path('app/', include('app.urls', namespace='app')),
]
