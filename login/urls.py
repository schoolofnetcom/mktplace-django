from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^register/success$', views.register_success, name='login_register_success'),
    url(r'^register$', views.register, name='login_register'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page':'/'}, name='logout'),

]