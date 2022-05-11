from django.shortcuts import render

from django.http import Http404
from issues_manager import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated # quoi le dernier def de base dans les settings
from django.contrib.auth import authenticate

from rest_framework import viewsets

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError
)


from .models import CustomUser
from .serializer import CustomUserSerializer, RegisterUserSerializer
from issues_manager.permissions import IsAdminAuthenticated


class AdminUserViewset(viewsets.ModelViewSet):
    """Vue réservée aux administrateurs
    Elle permet toutes les actions du CRUD sur les users
    """
    serializer_class = CustomUserSerializer
    queryset = users = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, IsAdminAuthenticated )


class UserView(APIView):
    """ List all users """
    
    def get(self,*args, **kwargs):
        """Attention : les args et kwargs semblent inutiles mais ça plante sans"""
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class RegisterUserView(APIView):
    """ create a new user """
    permission_classes = (AllowAny,)
    serializer_class= RegisterUserSerializer  # NB : si on ne met pas ça là on a pas de formulaire adequate à remplir

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = RegisterUserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)