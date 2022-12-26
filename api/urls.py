from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.infrastructure.ping_view import PingView
from .viewsets import BeerTapDispenserViewSet

app_name = 'api'

router = SimpleRouter()
router.register(r'dispenser', BeerTapDispenserViewSet)

urlpatterns = [
    path('ping', PingView.as_view()),
    path('', include(router.urls))
]
