import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_project.settings')

django_asgi_app = get_asgi_application()

def get_application():
    from channels.routing import URLRouter
    import question.routing

    return ProtocolTypeRouter({
        "http": django_asgi_app,
        "websocket": URLRouter(
            question.routing.websocket_urlpatterns
        ),
    })

application = get_application()
