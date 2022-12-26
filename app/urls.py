from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Dispenser Api",
        default_version='v1',
        description="Project build by osw4l",
        contact=openapi.Contact(email="ioswxd@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/', include('api.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
]
