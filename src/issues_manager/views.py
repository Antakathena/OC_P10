from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    ContributorsSerializer,
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.

class ProjectList(APIView):
    """  
    https://www.django-rest-framework.org/tutorial/3-class-based-views/  à lire en entier (mixin, generic...)
    """
    pass

class ProjectDetail(APIView):
    pass

class IssueList(APIView):
    pass

class IssueDetail(APIView):
    pass

class CommentList(APIView):
    pass

class CommentDetail(APIView):
    pass

class ContributorsList(APIView):
    pass

class ontributorsDetail(APIView):
    pass


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        "inscription":"/signup/, POST",
        "connexion":"/login/, POST",
        "déconnexion":"/logout/, GET",

        "récupérer la liste des projets autorisés":"/projects/, GET",

        "créer un projet":"/projects/, POST",
        "récupérer les détails d'un projet":"/projects/{\id}/, GET",
        "mettre à jour un projet":"/projects/{\id}/, PUT",
        "supprimer un projet et ses problèmes":"/projects/{\id}/DELETE",

        "ajouter un utilisateur (collaborateur) à un projet":"/projects/{\id}/users, POST",
        "récupérer la liste de tous les contributeurs d'un projet":"/projects/{\id}/users, GET",
        "retirer un contributeur d'un projet":"/projects/{\id}/users, DELETE",

        "créer un problème lié à un projet":"/projects/{\id}/issues, POST",
        "récupérer la liste des problèmes liés à un projet":"/projects/{\id}/issues, GET",
        "Mettre à jour un problème":"/projects/{\id}/issues, PUT",
        "supprimer un problème":"/projects/{\id}/issues, DELETE",

        "commenter un problème":"/projects/{\id}/issues/comments, POST",
        "récupérer les commentaires sur un problème":"/projects/{\id}/issues/comments, GET",
        "modifier son commentaire":"/projects/{\id}/issues, PUT",
        "supprimer son commentaire":"/projects/{\id}/issues, DELETE",
    }

    return Response(api_urls)