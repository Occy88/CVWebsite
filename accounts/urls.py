from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url, include
#----------URL'S AVAILABLE FOR ACTIVITIES RELATED TO USER MODEL SPECIFICALLY-------------
app_name = 'accounts'
urlpatterns = [
    # /account/

    url(r'^login/$', login, {'template_name': 'accounts/templates/registration/login.html'}, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', logout, {'template_name': 'accounts/templates/registration/logout.html'}, name='logout'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^password_reset/$', auth_views.password_reset,
        {'email_template_name': 'accounts/templates/registration/password_reset_email.html',
         'subject_template_name': 'accounts/templates/registration/password_reset_subject.txt',
         'post_reset_redirect': 'accounts:password_reset_done',
         'from_email': 'accounts/templates/registration/password_reset_email.html',
         }, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'accounts/templates/registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name':
                                                'accounts/templates/registration/password_reset_confirm.html',
                                            'post_reset_redirect': 'accounts:password_reset_complete'},
        name='password_reset_confirm'),
    url(r'^password_reset/complete/$', auth_views.password_reset_complete,
        {'template_name': 'accounts/templates/registration/password_reset_complete.html'},
        name='password_reset_complete'),
]
