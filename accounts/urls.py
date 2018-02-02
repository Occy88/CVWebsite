from django.urls import path
from django.conf.urls import url
from  django.contrib.auth.views import login, logout
from . import views
app_name='accounts'
urlpatterns = [
    #/files/
    path('', views.home, name='accounts'),
    url(r'^login/$',login,{'template_name':'accounts/templates/accounts/login.html'}),
    url(r'^register/$',views.register,name='register'),
    url(r'^logout/$',logout,{'template_name':'accounts/templates/accounts/logout.html'}),
    url(r'^profile/$',views.view_profile,name='profile'),
    url(r'^profile/edit$',views.edit_profile,name='profile'),
    url(r'^change-password/$',views.change_password,name='change_password')

    #/files/documents

]