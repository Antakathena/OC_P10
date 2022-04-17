from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import(
    Project,
    Issue,
    Comment,
    Contributors
)
from .serializers import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    ContributorsSerializer,
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
 

    

# Create your views here.

class ProjectViewSet(ModelViewSet):
    # pour passer la vue en lecture seule il suffit de changer l'héritage pour ReadOnlyModelViewset

    serializer_class = ProjectSerializer

    def get_queryset(self):
        permission_classes = [IsAuthenticated] # ?????
        project_id = self.request.GET.get(id)
        if project_id is not None:
            queryset = queryset.filter(project_id = project_id)
        else:
            queryset = Project.objects.all()
        return queryset

@action(methods=['post'], detail=True, )
class IssueViewSet(ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        issue_id = self.request.GET.get(id)
        if issue_id is not None:
            queryset = queryset.filter(issue_id = issue_id)
        else:
            queryset = Issue.objects.all()
        return queryset

        # url('/<project>/<id>/issue/<id>', f)

class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        comment_id = self.request.GET.get(id)
        if comment_id is not None:
            queryset = queryset.filter(comment_id = comment_id)
        else:
            queryset = Comment.objects.all()
        return queryset

# class ProjectListView(APIView):
#     """  
#     https://www.django-rest-framework.org/tutorial/3-class-based-views/  à lire en entier (mixin, generic...)
#     List all projects, or create a new project.
#     """

#     def get(self, *args, **kwargs):
#         projects = Project.objects.all()
#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     pass

@api_view(['GET'])
def api_overview(request):
    """
    Une vue simple pour avoir un aperçu des ENDPOINTS demandés
    les r avant les guillemets servent à indiquer que tout est à prendre comme string
    """

    api_urls = {
        "inscription":"  /signup/, POST",
        "connexion":"  /login/, POST",
        "déconnexion":"  /logout/, GET",

        "récupérer la liste des projets autorisés":"  /projects/, GET",

        "créer un projet":"  /projects/, POST",
        "récupérer les détails d'un projet":r"  /projects/{id}/, GET",
        "mettre à jour un projet":r"  /projects/{id}/, PUT",
        "supprimer un projet et ses problèmes":r"  /projects/{id}/DELETE",

        "ajouter un utilisateur (collaborateur) à un projet":r"  /projects/{id}/users, POST",
        "récupérer la liste de tous les contributeurs d'un projet":r"  /projects/{id}/users, GET",
        "retirer un contributeur d'un projet":r"  /projects/{id}/users, DELETE",

        "créer un problème lié à un projet":r"  /projects/{id}/issues, POST",
        "récupérer la liste des problèmes liés à un projet":r"  /projects/{id}/issues, GET",
        "Mettre à jour un problème":r"  /projects/{id}/issues, PUT",
        "supprimer un problème":r"  /projects/{id}/issues, DELETE",

        "commenter un problème":r"  /projects/{id}/issues/comments, POST",
        "récupérer les commentaires sur un problème":r"  /projects/{id}/issues/comments, GET",
        "modifier son commentaire":r"  /projects/{id}/issues, PUT",
        "supprimer son commentaire":r"  /projects/{id}/issues, DELETE",
    }

    return Response(api_urls)