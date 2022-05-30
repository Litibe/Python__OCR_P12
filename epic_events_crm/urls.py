from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as DRF_jwt_views

from authentication.views import UserSignUpView
from crm.views_API import ContractViews, EventViews
from crm.views_API import NeedViews, CustomerViews
from crm.views import main_page

admin.site.site_header = "EpicEvents CRM"
admin.site.site_title = "EpicEvents CRM Portal"
admin.site.index_title = "Welcome to EpicEvents CRM Portal"

urlpatterns = [
     path('', main_page, name='homepage'),
     path('portal/', admin.site.urls),
     path('api/authentication/login/',
          DRF_jwt_views.TokenObtainPairView.as_view(), name='login'),
     path('api/authentication/login/refresh/',
          DRF_jwt_views.TokenRefreshView.as_view(),
          name='login_refresh'),
     path('api/authentication/signup/',
          UserSignUpView.as_view(
             {'post': "create_a_new_user"}), name='sign_up'),

     path('api/crm/customer/',
          CustomerViews.as_view(
             {'get': "read_customer",
              'post': 'create_customer'
              }), name='customers'),
     path('api/crm/customer/<id_customer>/',
          CustomerViews.as_view(
             {"get": "details_customer",
              "put": "put_customer",
              'delete': 'delete_customer'}), name='customer'),

     path('api/crm/contract/',
          ContractViews.as_view(
             {'get': "read_contract",
              'post': 'create_contract'}), name='contracts'),
     path('api/crm/contract/<id_contract>/',
          ContractViews.as_view(
              {'get': "details_contract",
               'put': "put_contract",
               'delete': 'delete_contract'}), name='contract'),

     path('api/crm/event/',
          EventViews.as_view(
             {'get': "read_event",
              'post': 'create_event'
              }), name='events'),
     path('api/crm/event/<id_event>/',
          EventViews.as_view(
              {'get': "details_event",
               'put': 'put_event',
               'delete': 'delete_event'
               }), name='event'
          ),

     path('api/crm/need/',
          NeedViews.as_view(
             {'get': "read_need",
              'post': 'create_need'}), name='needs'),
     path('api/crm/need/<id_need>/',
          NeedViews.as_view(
              {'get': "details_need",
               'put': 'put_need',
               'delete': "delete_need",
               }), name='need'
          ),
]
