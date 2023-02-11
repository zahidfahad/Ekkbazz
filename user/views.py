from .models import *
from . import serializers
from rest_framework.views import APIView
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from django.views.generic.base import TemplateView
from django.utils.safestring import mark_safe
from common.responses import (
    success_response,error_response,
    ListPagination,VALIDATION_ERROR
)
from common.utils import (
    Auth,
)


# Create your views here.


#quick register
class RegisterUser(APIView):
    serializer_class = serializers.RegisterSerializer
    message = ''
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.message = _("User Created")
            return success_response(201,self.message,serializers.ViewAccountSerializer(user,context={"request":request}).data)
        return error_response(400,VALIDATION_ERROR,**serializer.custom_errors)
    

class LoginApi(APIView):
    serializer_class = serializers.AuthTokenSerializer
    message = ""
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return error_response(400,VALIDATION_ERROR,**serializer.custom_errors)
        
        user = serializer.validated_data['user']
        login(request,user)
        self.message = _("Login Succeeded")
        return success_response(200, self.message, Auth().get_tokens_for_user(user))
    
    
class BusinessView(APIView, ListPagination):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.BusinessSerializer
    message = ""
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.message = _("Business added.")
            return success_response(201,self.message,serializer.data)
        return error_response(400,VALIDATION_ERROR,**serializer.custom_errors)
    
    def get(self, request, *args, **kwargs):
        latitude = request.query_params.get('lat')
        longitude = request.query_params.get('lng')
        queryset = Business.nearby(latitude,longitude,2000)
        paginated_queryset = self.paginate_queryset(queryset,request=request)
        self.message = _("Business List")
        return self.get_paginated_response(self.message,paginated_queryset)
    
    
class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_doc_button = """ <a class='btn btn-success' href={}>{}</a> """.format('/docs/', 'View Docs')
        admin_panel_button = """ <a class='btn btn-success' href={}>{}</a> """.format('/admin/', 'Go to admin')
        context['doc_btn'] = mark_safe(api_doc_button)
        context['admin_btn'] = mark_safe(admin_panel_button)
        return context