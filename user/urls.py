from django.urls import path
from .views import *

urlpatterns = [
    path('register-user/', RegisterUser.as_view(), name = 'register_user'),
    path('login/', LoginApi.as_view(), name = 'login_api'),
    path('business/', BusinessView.as_view(), name = 'business_view'),
]