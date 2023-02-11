from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _



class ViewAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','is_active']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']
        
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        return user
    
    @property
    def custom_errors(self):
        # returning custom error messages
        default_errors = self.errors
        errors_messages = []
        for field_name, field_errors in default_errors.items():
            for field_error in field_errors:
                error_message = '%s: %s'%(field_name, field_error)
                errors_messages.append(error_message)
        return {'errors': errors_messages}


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    access = serializers.CharField(
        label=_("Access Token"),
        read_only=True
    )
    refresh = serializers.CharField(
        label=_("Refresh Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        request = self.context.get('request')

        if username and password:
            user = authenticate(request=request,username=username,password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    @property
    def custom_errors(self):
        # returning custom error messages
        default_errors = self.errors
        errors_messages = []
        for field_name, field_errors in default_errors.items():
            for field_error in field_errors:
                error_message = '%s: %s'%(field_name, field_error)
                errors_messages.append(error_message)
        return {'errors': errors_messages}
    

class BusinessSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_digits=30,decimal_places=25,required=True)
    longitude = serializers.DecimalField(max_digits=30,decimal_places=25,required=True)
    
    class Meta:
        model = Business
        fields = '__all__'
        
    @property
    def custom_errors(self):
        # returning custom error messages
        default_errors = self.errors
        errors_messages = []
        for field_name, field_errors in default_errors.items():
            for field_error in field_errors:
                error_message = '%s: %s'%(field_name, field_error)
                errors_messages.append(error_message)
        return {'errors': errors_messages}