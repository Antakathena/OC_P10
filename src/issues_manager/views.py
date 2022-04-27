from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import(
    Project,
    Issue,
    Comment,
    Contributor
)
from .serializers import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    ContributorsSerializer,
)
from .permissions import IsAdminAuthenticated, IsAuthorPermission
    

# Create your views here.

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated,] # pour get et post : contributeur du projet, pour delete et put : owner
    # pour passer la vue en lecture seule il suffit de changer l'héritage pour ReadOnlyModelViewset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated,]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, ] # IsCollaborating quand c'est prêt
        else:
            permission_classes = [IsAuthenticated, IsAuthorPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        project_id = self.request.GET.get(id)
        if project_id is not None:
            queryset = queryset.filter(project_id = project_id)
        else:
            queryset = Project.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IssueViewSet(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated,]

    # exemple avec nested router : def get_queryset(self):
    # return Issue.objects.filter(project = self.kwargs['project_pk'])

    @action(methods=['get', 'post'], detail=True)
    # , url_path='project/(?<project_pk>[^/.]+)')
    def get_queryset(self):
        issue_id = self.request.GET.get(id)
        
        if issue_id is not None:
            queryset = queryset.filter(issue_id = issue_id)
            issue = self.queryset.get(issue_id = issue_id, project_id = self.kwargs['project_pk'])
            return issue
        else:
            queryset = Issue.objects.all()
            return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        comment_id = self.request.GET.get(id)
        if comment_id is not None:
            queryset = queryset.filter(comment_id = comment_id)
            comment = self.queryset.get(comment_id = comment_id, issue_id = self.kwargs['issue_id'], project_id = self.kwargs['project_pk'])
            return comment
        else:
            queryset = Comment.objects.all()
            return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ContributorViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        contributor_id = self.request.GET.get(id)
        if contributor_id is not None:
            queryset = queryset.filter(contributor_id = contributor_id)
            contributor = self.queryset.get(contributor_id = contributor_id) #, project_id = self.kwargs['project_pk'])
            return contributor
        else:
            queryset = Contributor.objects.all()
            return queryset


@api_view(['GET'])


def api_overview(request):
    """
    Une vue simple pour avoir un aperçu des ENDPOINTS demandés
    les r avant les guillemets servent à indiquer que tout est à prendre comme string
    """
    
    # if request.user.is_authenticated:
    #     utilisateur = {  }
    # else :
    #     utilisateur = { "Vous n'êtes pas connecté" :"anonyme" ,}


    api_urls = {
        "Vous être connecté en tant que" : f"{request.user}\n\n",
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