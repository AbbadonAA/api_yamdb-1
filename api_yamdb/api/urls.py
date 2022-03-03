from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'
API_VERSION_1 = 'v1/'

router_v1 = DefaultRouter()
router_v1.register('users', views.UsersViewSet, basename='users')
router_v1.register(
    'categories',
    views.CategoryViewSet,
    basename='categories')
router_v1.register(
    'genres',
    views.GenreViewSet,
    basename='genres')
router_v1.register(
    'titles',
    views.TitleViewSet,
    basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments'
)

auth_urls = [
    path('signup/', views.APISignup.as_view()),
    path('token/', views.APIGetToken.as_view())
]

urlpatterns = [
    path(API_VERSION_1, include(router_v1.urls)),
    path(API_VERSION_1 + 'auth/', include(auth_urls)),
]
