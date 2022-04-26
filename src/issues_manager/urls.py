from django.urls import path, include
from rest_framework import routers  # est-ce que ça va là ou dans les urls globales?
# Un router permet de définir en une seule fois toutes les opérations du CRUD sur un endpoint.
from rest_framework_nested import routers

from . import views
from .views import(
    # ProjectListView,
    ProjectViewSet,
    IssueViewSet,
    CommentViewSet,
)

router = routers.SimpleRouter()
# pourquoi un r devant ici; et regex ou pas après? Et SimpleRouter() ou DefaultRouter() alors?
# https://teamtreehouse.com/community/what-is-the-difference-between-use-simplerouter-and-defaultrouter-classes-2
router.register('projects', ProjectViewSet, basename='projects') 
router.register('issues', IssueViewSet, basename='issues')
router.register('comments', CommentViewSet, basename='comments')

# url('/<pk_project>/issue/<issue_id>', f) viewset imbriqués avec un plugin ? cf liens sur le discord
projects_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
projects_router.register('issues', IssueViewSet, basename='project-issues')


urlpatterns = [
    path('', views.api_overview, name="api-overview"),
    # path('issues_manager/projects/', ProjectListView.as_view(), name="projects"),
    path('', include(router.urls)),

    path('', include(projects_router.urls)),

]
