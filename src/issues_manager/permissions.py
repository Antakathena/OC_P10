from rest_framework.permissions import BasePermission

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
 
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
    message = "Seul l'auteur peut modifier ou supprimer son post" # delete et put patch

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            print("author should access to all methods on their posts")
            return True
        elif request.user.is_authenticated and request.method in SAFE_METHODS:
            print("collaborators should be able to read and post issues to projects or comments to issues")
            return True
        else :
            return False

    
    pass

# pour issues et comments, ajouter un related name ou @property owner devrait suffir?