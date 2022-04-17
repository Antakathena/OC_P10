from django.contrib.auth.models import AbstractUser, PermissionsMixin

# from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return f"{self.first_name} {self.last_name}, as {self.username}, id:{self.id}"