from django.urls import path
from django.conf.urls import url
from  django.contrib.auth.views import login, logout,password_reset,password_reset_done,password_reset_confirm,password_reset_complete
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url, include
app_name='accounts'
urlpatterns = [
    #/files/

    path('', views.home, name='accounts'),

    url(r'^login/$',login,{'template_name':'accounts/templates/registration/login.html'},name='login'),
    url(r'^register/$',views.register,name='register'),
    url(r'^logout/$',logout,{'template_name':'accounts/templates/registration/logout.html'},name='logout'),
    url(r'^profile/$',views.view_profile,name='profile'),
    url(r'^profile/edit/$',views.edit_profile,name='profile'),
    url(r'^change-password/$',views.change_password,name='change_password'),
    #//--------dont have time for this---------------
    url(r'^password_reset/$', auth_views.password_reset,{'email_template_name':'accounts/templates/registration/password_reset_email.html',
                                                    'subject_template_name': 'accounts/templates/registration/password_reset_subject.txt',
                                                    'post_reset_redirect':'accounts:password_reset_done',
                                                    'from_email':'accounts/templates/registration/password_reset_email.html',
                                                    },name='password_reset'),

    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'accounts/templates/registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.password_reset_confirm),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]