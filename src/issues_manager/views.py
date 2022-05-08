from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)

from rest_framework.decorators import action

from .models import (
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
from .permissions import IsCollaboratingPermission, IsAuthorPermission
    

class ProjectViewSet(ModelViewSet):
    """
    Classe des projets.
    Tout les utilisateurs authentifiés peuvent créer un projet (POST/create_Project).
    Seul l'auteur peut modifier ou supprimer le projet (retrieve, update, destroy_Project).
    Seuls les contributeurs peuvent voir les détails du projet (GET/list_Project),
    et notifier un problème pour ce projet (POST/create_Issue).
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ]
        

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        print(obj)
        return obj

    def get_permissions(self):
        """ gets permissions
        Instantiates and returns the list of permissions that this view requires.
        # pour get et post : contributeur du projet, pour delete et put : author
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, IsCollaboratingPermission, ]
        else:
            permission_classes = [IsAuthenticated, IsAuthorPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """ gets list of projects or a specific project
        If a project_id is given, gets a specific project,
        else gets all projects for the connected user if no id has been given
        """
        project_id = self.request.GET.get(id)
        if project_id is not None:
            queryset = Project.objects.filter(id=project_id)
        else:
            queryset = Project.objects.filter(contributor__user = self.request.user)

        return queryset

    def perform_create(self, serializer):
        """designate creator as author of the instance"""
        serializer.save(author=self.request.user)

    def list(self, request,):
        """used by nested urls"""
        queryset = Project.objects.filter(contributor__user = self.request.user)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """used by nested urls"""
        queryset = Project.objects.filter(contributor__user = self.request.user)
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class IssueViewSet(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, ]

    # exemple avec nested router : def get_queryset(self):
    # return Issue.objects.filter(project = self.kwargs['project_pk'])

    @action(methods=['get', 'post'], detail=True)
    # , url_path='project/(?<project_pk>[^/.]+)')
    def get_queryset(self, *arg, **kwargs):
        issue_id = self.request.GET.get(id)
        queryset = Issue.objects.filter(project__contributor__user = self.request.user)
        
        if issue_id is not None:
            queryset = queryset.filter(id=issue_id)
            # nb 28/04/2022 remplacé queryset.filter par Issue.objects.filter
            issue = queryset.get(issue_id=issue_id, project=self.kwargs['project_pk'])
            return issue
        else:
            project_issues = queryset.filter(project=self.kwargs['project_pk'])
            return project_issues

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, project_pk=None, **kwarg):
        queryset = Issue.objects.filter(project=project_pk)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None):
        queryset = Issue.objects.filter(pk=pk, project=project_pk)
        issue = get_object_or_404(queryset, pk=pk)
        serializer = IssueSerializer(issue)
        return Response(serializer.data)
    

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        comment_id = self.request.GET.get(id)
        if comment_id is not None:
            queryset = Comment.objects.filter(comment_id=comment_id)
            # nb 28/04/2022 remplacé queryset.filter par Comment.objects.filter
            comment = self.queryset.get(
                comment_id=comment_id,
                issue_id=self.kwargs['issue_id'],
                project_id=self.kwargs['project_id']
            )
            return comment
        else:
            queryset = Comment.objects.all()
            return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def list(self, request, project_pk=None, issues_pk=None):
        queryset = Comment.objects.filter(
            issue__project=project_pk,
            issue=issues_pk
        )
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None, issues_pk=None):
        queryset = Comment.objects.filter(pk=pk, issue__project=project_pk, issue=issues_pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


class ContributorViewSet(ModelViewSet):

    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        contributor_id = self.request.GET.get(id)
        if contributor_id is not None:
            queryset = Contributor.objects.filter(contributor_id=contributor_id)
            # nb 28/04/2022 remplacé queryset.filter par Contributor.objects.filter
            contributor = self.queryset.get(contributor_id=contributor_id)
            # project_id = self.kwargs['project_pk'])
            return contributor
        else:
            queryset = Contributor.objects.all()
            return queryset


class AdminProjectViewset(ModelViewSet):
    """Vues reservée aux administrateurs
    Elle permet toutes les actions du CRUD sur les projets"""
    serializer_class = ProjectSerializer
    queryset = projects = Project.objects.all()  
    permission_classes = (IsAuthenticated, IsAdminUser)
    

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

    infos = {
        "Bienvenue dans l'API SoftDesk.\
            Vous être connecté en tant que": f"{request.user}",

        "inscription": "  /signup/, POST",
        "connexion": "  /login/, POST",
        "déconnexion": "  /logout/, GET",

        "récupérer la liste des projets autorisés": "  /projects/, GET",

        "créer un projet": "  /projects/, POST",
        "récupérer les détails d'un projet": r"  /projects/{id}/, GET",
        "mettre à jour un projet": r"  /projects/{id}/, PUT",
        "supprimer un projet et ses problèmes": r"  /projects/{id}/DELETE",

        "ajouter un utilisateur (collaborateur) à un projet": r"  /projects/{id}/users, POST",
        "récupérer la liste de tous les contributeurs d'un projet": r"  /projects/{id}/users, GET",
        "retirer un contributeur d'un projet": r"  /projects/{id}/users, DELETE",

        "créer un problème lié à un projet": r"  /projects/{id}/issues, POST",
        "récupérer la liste des problèmes liés à un projet": r"  /projects/{id}/issues, GET",
        "Mettre à jour un problème": r"  /projects/{id}/issues, PUT",
        "supprimer un problème": r"  /projects/{id}/issues, DELETE",

        "commenter un problème": r"  /projects/{id}/issues/comments, POST",
        "récupérer les commentaires sur un problème": r"  /projects/{id}/issues/comments, GET",
        "modifier son commentaire": r"  /projects/{id}/issues, PUT",
        "supprimer son commentaire": r"  /projects/{id}/issues, DELETE",
    }
    return Response(infos)
