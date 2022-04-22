from django.contrib.auth import views as auth_views
from django.urls import path
# from rest_framework_jwt.views import obtain_jwt_token /non : plus maintenu
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserView, RegisterUserView, AuthenticateUser, AdminUserViewset

app_name = 'users'  # pour utiliser namespace dans les urls

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # url(r'^api-token-auth/', obtain_jwt_token), /non : plus maintenu
    # va avec : from django.conf.urls import url # à étudier
    path('userslist/', UserView.as_view()),
    path('signup/', RegisterUserView.as_view()),
    path('login/', AuthenticateUser.as_view(), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

router = DefaultRouter()
router.register('user', AdminUserViewset, basename ='user')

urlpatterns += router.urls