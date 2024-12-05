
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls', namespace='web')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('question/', include('question.urls', namespace='question')),
]
