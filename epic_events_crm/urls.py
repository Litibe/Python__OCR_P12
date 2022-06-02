from django.contrib import admin
from django.urls import path, re_path
from rest_framework_simplejwt import views as DRF_jwt_views

from authentication.views import UserSignUpView
from crm.API.API_customer import CustomerViews
from crm.API.API_contract import ContractViews
from crm.API.API_event import EventViews
from crm.API.API_need import NeedViews
from crm.views.homepage import main_page

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
     path('api/crm/customer/id/<id_customer>/',
          CustomerViews.as_view(
             {"get": "details_customer",
              "put": "put_customer",
              'delete': 'delete_customer'}), name='customer'),
     path('api/crm/customer/mail/<mail>/',
          CustomerViews.as_view(
               {'get': "search_mail_customer"}), name='customer_search_mail'),
     path('api/crm/customer/name/',
          CustomerViews.as_view(
               {'get': "search_name_customer"}), name='customer_search_name'),
     path('api/crm/customer/salescontact/<mail>/',
          CustomerViews.as_view(
               {'get': "search_sales_contact_customer"}),
          name='customer_search_sales'),

     path('api/crm/contract/',
          ContractViews.as_view(
             {'get': "read_contract",
              'post': 'create_contract'}), name='contracts'),
     re_path(r'^api/crm/contract/amount/(?P<amount>\d{1,8}[$]?)/$',
             ContractViews.as_view(
               {'get': "search_contract_by_amount"}),
             name='contract_by_amount'),
     path('api/crm/contract/id/<id_contract>/',
          ContractViews.as_view(
              {'get': "details_contract",
               'put': "put_contract",
               'delete': 'delete_contract'}), name='contract'),
     re_path(r'^api/crm/contract/date/start/(?P<date>\d{4}-\d{2}-\d{2})/$',
             ContractViews.as_view(
               {'get': "search_contract_by_date_start"}),
             name='contract_by_date_start'),
     re_path(r'^api/crm/contract/date/end/(?P<date>\d{4}-\d{2}-\d{2})/$',
             ContractViews.as_view(
               {'get': "search_contract_by_date_end"}),
             name='contract_by_date_end'),
     path('api/crm/contract/mail/<mail>/',
          ContractViews.as_view(
               {'get': "search_contract_mail_customer"}),
          name='contract_by_email_customer'),
     path('api/crm/contract/name/',
          ContractViews.as_view(
               {'get': "search_contract_by_name_customer"}),
          name='contract_by_name_customer'),

     path('api/crm/event/',
          EventViews.as_view(
             {'get': "read_event",
              'post': 'create_event'
              }), name='events'),
     path('api/crm/event/id/<id_event>/',
          EventViews.as_view(
              {'get': "details_event",
               'put': 'put_event',
               'delete': 'delete_event'
               }), name='event'
          ),
     re_path(r'^api/crm/event/date/start/(?P<date>\d{4}-\d{2}-\d{2})/$',
             EventViews.as_view(
               {'get': "search_event_by_date_start"}),
             name='event_by_date_start'),
     re_path(r'^api/crm/event/date/end/(?P<date>\d{4}-\d{2}-\d{2})/$',
             EventViews.as_view(
               {'get': "search_event_by_date_end"}),
             name='event_by_date_end'),
     path('api/crm/event/mail/<mail>/',
          EventViews.as_view(
               {'get': "search_event_mail_customer"}),
          name='event_by_email_customer'),
     path('api/crm/event/name/',
          EventViews.as_view(
               {'get': "search_event_by_name_customer"}),
          name='event_by_name_customer'),

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
