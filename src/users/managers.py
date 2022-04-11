from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import ugettext_lazy as _
# des _ étaient mis ainsi : raise ValueError(_('The Email must be set'))
# plus dispo in django v3+

class CustomUserManager(BaseUserManager):
    pass