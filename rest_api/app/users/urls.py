from django.urls import path
import users.views as users_views
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', users_views.UserCreateView.as_view(), name='create'),
    path('update/', users_views.UserUpdateView.as_view(), name='user-update'),
    path('', users_views.UserListView.as_view(), name='user-list')
]
