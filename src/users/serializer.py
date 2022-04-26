from issues_manager.models import Project
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    # projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all()) ##
    
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'username',
                  'date_joined', 'password',) ## 'projects'
        
        extra_kwargs = {'password': {'write_only': True}}

class RegisterUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name','username',
                  'date_joined', 'password', )
        
        extra_kwargs = {'password': {'write_only': True}, 'first_name': {'required': True}, 'last_name': {'required': True},'username': {'required': True} }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            is_active = True,
            )
        return user

