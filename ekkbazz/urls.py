from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import HomeView
# for swagger docs
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Ekkbazz API",
      default_version='v1',
      description="This doc covers Ekkbazz API scecifications",
      terms_of_service="#",
      contact=openapi.Contact(email="zh.fahad123@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
# ends swagger


app_urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
]


jwt_urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

doc_urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns = app_urlpatterns+jwt_urlpatterns+doc_urlpatterns