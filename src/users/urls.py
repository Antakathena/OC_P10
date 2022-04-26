from django.contrib.auth import views as auth_views
from django.urls import path
# from rest_framework_jwt.views import obtain_jwt_token /non : plus maintenu
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserView, RegisterUserView, AuthenticateUser, AdminUserViewset, GetTokens, RefreshToken
# from django.conf.urls import url # à étudier

app_name = 'users'  # pour utiliser namespace dans les urls

urlpatterns = [
    # path('token/', GetTokens.as_view(), name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', RefreshToken.as_view(), name='token_refresh'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # non plus maintenu : url(r'^api-token-auth/', obtain_jwt_token),
    path('userslist/', UserView.as_view()),
    path('signup/', RegisterUserView.as_view()),
    path('login/', AuthenticateUser.as_view(), name='login'),
]

router = DefaultRouter()
router.register('user', AdminUserViewset, basename ='user')

urlpatterns += router.urls