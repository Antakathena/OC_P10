from django.urls import path, include
from rest_framework import routers  # est-ce que ça va là ou dans les urls globales?
# Un router permet de définir en une seule fois toutes les opérations du CRUD sur un endpoint.
from rest_framework_nested import routers
# https://pypi.org/project/drf-nested-routers/

from . import views
from .views import(
    # ProjectListView,
    ProjectViewSet,
    IssueViewSet,
    CommentViewSet,
    ContributorViewSet
)

router = routers.SimpleRouter()
# pourquoi un r devant ici; et regex ou pas après? Et SimpleRouter() ou DefaultRouter() alors?
# https://teamtreehouse.com/community/what-is-the-difference-between-use-simplerouter-and-defaultrouter-classes-2
router.register('projects', ProjectViewSet, basename='projects') 
# router.register('issues', IssueViewSet, basename='issues') # a retirer a priory, doublon avec project/id/issues/id
# router.register('comments', CommentViewSet, basename='comments') # idem
router.register('contributors', ContributorViewSet, basename='contributors') # idem

# url('/<pk_project>/issue/<issue_id>', f) viewset imbriqués avec un plugin ? cf liens sur le discord
projects_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
projects_router.register('issues', IssueViewSet, basename='project-issues')

# projects_router.register('users', ContributorViewSet, basename='project-users')

# issues_router = routers.NestedSimpleRouter(router, 'issues', lookup='issues')
# issues_router.register('comments', CommentViewSet, basename='issue-comments')


urlpatterns = [
    path('', views.api_overview, name="api-overview"),
    # path('issues_manager/projects/', ProjectListView.as_view(), name="projects"),
    path('', include(router.urls)),

    path('', include(projects_router.urls)),
    # path('', include(issues_router.urls)),

]
