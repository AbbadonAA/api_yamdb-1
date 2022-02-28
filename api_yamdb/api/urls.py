from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views
from users.views import APISignup, APIGetToken, UsersViewSet


app_name = 'api'
API_VERSION_1 = 'v1/'

router_v1 = DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')


auth_urls = [
    path('signup/', APISignup.as_view()),
    path('token/', APIGetToken.as_view())
]

urlpatterns = [
    path(API_VERSION_1, include(router_v1.urls)),
    path(API_VERSION_1 + 'auth/', include(auth_urls)),
]