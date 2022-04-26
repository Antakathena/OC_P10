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
# Create your views here.

class AdminUserViewset(viewsets.ModelViewSet):
    """Changer la permission pour réserver cette vue aux administrateurs
    Elle permet toutes les actions du CRUD sur les users"""
    serializer_class = CustomUserSerializer
    queryset = users = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, ) # quand ok on peut remettre Isadminauthenticated


class UserView(APIView):
    """
    List all users
    """
    def get(self,*args, **kwargs):
        """Attention : les args et kwargs semblent inutile mais ça plante sans"""
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
"""
class RegisterUserView(APIView):
    serializer_class= RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user":CustomUserSerializer(user, context=self.get_serializer_context()).data, "message":"User Created Successfully.Now perform login to get your token",})

"""
class RegisterUserView(APIView):
    """
    create a new user
    Marche mais ajouter de quoi rentre obligatoire : validator? required?
    first_name et last_name
    """
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)
    serializer_class= RegisterUserSerializer  # NB : si on ne met pas ça là on a pas de formulaire adequate à remplir

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = RegisterUserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # comment ajouter un message, "l'utilisateur untel a bien été créé" ?
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokens(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        print( request.data, args, kwargs)
        serializer = self.get_serializer(data=request.data)
        print(serializer)

        try:
            serializer.is_valid(raise_exception=True)
            print("OK\n\n")
        except Exception as e:
            print(e)
            raise
        except TokenError as e:
            print("erreur\n")
            raise InvalidToken(e.args[0])

class RefreshToken(TokenRefreshView):
    permission_classes = (AllowAny,)


class AuthenticateUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            email = request.data.get('email', None) # email = request.data['email'] # 
            password = request.data.get('password', None) # request.data['password'] 

            try:    
                # user = authenticate(email=email, password=password) 
                user = CustomUser.objects.get(email=email, password=password)
            except models.Model.DoesNotExist as e:
                print("pas trouvé")
                print( email,  password)
                raise e
            else:
                print(user)

            if user:

                try:
                    # là c'est ce qui est donné dans le tuto nul, trouver la bonne solution
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {}
                    user_details['name'] = "%s %s" % (
                        user.first_name, user.last_name)
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)
    
                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a email and a password'}
            return Response(res)

"""
Tuto indiqué dans le projet
                # plop : reprendre le tuto : https://code.tutsplus.com/tutorials/how-to-authenticate-with-jwt-in-django--cms-30460
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {}
                    user_details['name'] = "%s %s" % (
                        user.first_name, user.last_name)
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)
    
                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a email and a password'}
            return Response(res)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
 
    try:
        email = request.data['email']
        password = request.data['password']
 
        user = User.objects.get(email=email, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
 
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)


# Tester d'abord authenticate users


Class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
 
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
 
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)
 
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
 
        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
 
        return Response(serializer.data, status=status.HTTP_200_OK)

"""