from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as DRF_jwt_views

from authentication.views import UserSignUpView


urlpatterns = [
    path('crm/', admin.site.urls),
    path('api/authentication/login/', DRF_jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('api/authentication/login/refresh/', DRF_jwt_views.TokenRefreshView.as_view(),
         name='login_refresh'),
    path('api/authentication/signup/', UserSignUpView.as_view(
             {'post': "create_a_new_user"}), name='sign_up'),
]
