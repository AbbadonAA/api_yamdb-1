# from django.urls import include, path
# from rest_framework.routers import DefaultRouter

# from .views import APISignup, APIGetToken, UsersViewSet

# router_v1 = DefaultRouter()
# router_v1.register('users', UsersViewSet, basename='users')

# auth_urls = [
#     path('signup/', APISignup.as_view()),
#     path('token/', APIGetToken.as_view())
# ]

# urlpatterns = [
#     path('v1/', include(router_v1.urls)),
#     path('v1/auth/', include(auth_urls)),
# ]