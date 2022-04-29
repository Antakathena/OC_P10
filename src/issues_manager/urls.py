from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers
# https://pypi.org/project/drf-nested-routers/

from . import views
from .views import(
    ProjectViewSet,
    IssueViewSet,
    CommentViewSet,
    ContributorViewSet,
    AdminProjectViewset,    
    # ProjectIssuesView
)

router = routers.SimpleRouter()
router.register('projects', ProjectViewSet, basename='projects')

# Les trois suivantes sont à retirer quand les nested routers ou les vues imbriquées marcheront:
# router.register('issues', IssueViewSet, basename='issues') # a retirer à la fin
# router.register('comments', CommentViewSet, basename='comments') # idem
# router.register('contributors', ContributorViewSet, basename='contributors') # idem

# On créé les nested routers :
projects_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
projects_router.register('issues', IssueViewSet, basename='project-issues')

projects_router.register('users', ContributorViewSet, basename='project-users')

issues_router = routers.NestedSimpleRouter(projects_router, 'issues', lookup='issues')
issues_router.register('comments', CommentViewSet, basename='issue-comments')


urlpatterns = [
    path('', views.api_overview, name="api-overview"),
    # path('issues_manager/projects/', ProjectListView.as_view(), name="projects"),
    path('', include(router.urls)),

    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),

    # path('projects/<project_id>/issues/', ProjectIssuesView.as_view())
]

# Celui-ci c'est juste pour étudier le syst. et avoir un accès admin pour gérer les utilisateurs :
router = routers.DefaultRouter()
router.register('admin-projects', AdminProjectViewset, basename ='admin-projects')

urlpatterns += router.urls
