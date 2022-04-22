from rest_framework.permissions import BasePermission
 
class IsAdminAuthenticated(BasePermission):
    """autorisations de superuser/Admin"""
 
    def has_permission(self, request, view):
    # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

class IsCollaborating(BasePermission):
    """autorisation de contributeur au projet, sachant que is authenticated ne suffit pas :
    il faut savoir à quels projets l'utilisateur est associé (one to many)"""
    pass

# pour issues et comments, ajouter un related name ou @property owner devrait suffir?