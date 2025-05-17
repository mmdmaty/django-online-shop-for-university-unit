from django.urls import path
from . import views
urlpatterns = [
    path(route ='info/',view=views.AccountDetails.as_view(),name='account_name'),
    path(route ='test/',view=views.test_form_view,name='test'),
]