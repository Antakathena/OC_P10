from rest_framework.permissions import BasePermission
 
class IsAdminAuthenticated(BasePermission):
    pass
    """autorisations de superuser/Admin"""
 
    def has_permission(self, request, view):
    # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

class IsCollaborating(BasePermission):
    """autorisation de contributeur au projet, sachant que is authenticated ne suffit pas :
    il faut savoir à quels projets l'utilisateur est associé (one to many)"""
    
    # = participe au projet en question
    # hériter de DjangoModelPermission (get et post ok)?  

    pass

class IsAuthorPermission(BasePermission):
    message = "Seul l'auteur peut modifier ou supprimer son post"

    def has_object_permission(self, request, view, obj):
        return bool(obj.author == request.user)  #request.method is SAFE_METHODS:  get, options or head

    # delete et put patch
    pass

# pour issues et comments, ajouter un related name ou @property owner devrait suffir?