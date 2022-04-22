from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from users.managers import CustomUserManager

# from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser, PermissionsMixin):
    """Créé au début au cas où il faille une adaptation ultérieure.
    Les champs par défaut sont :
    id, password, last_login, is_superuser, username, fist_name,
    last_name, email, is_staff, is_active, date_joined, groups, user_permissions
    
    puis suivi du modèle donné dans la ressource du doc "sérurité":
    https://code.tutsplus.com/tutorials/how-to-authenticate-with-jwt-in-django--cms-30460

    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
 
    """
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30) # il faut choisir : blank = True ou required field?
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
 
    objects = CustomUserManager()
 
    # USERNAME_FIELD = 'email' commenté parce que le username se transforme en e-mail à l'enregistrement sinon
    REQUIRED_FIELDS = ['first_name', 'last_name']
 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self

    

    def __str__(self):
        return f"{self.first_name} {self.last_name}, id:{self.id}"