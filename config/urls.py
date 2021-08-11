from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi


schema_url_patterns = [
    path('api/', include('api.urls')),
    path('movie/', include('movie.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="MOVIE BACKEND API",
        default_version='v1',
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('movie/', include('movie.urls')),
]
if settings.DEBUG:
    urlpatterns += [
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]