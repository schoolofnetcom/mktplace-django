from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^my_products$', views.my_products, name='my_products'),
    url(r'^product/new$', views.product_new, name='product_new'),
    url(r'^product/edit/(?P<product_id>[\d]+)$', views.product_edit, name='product_edit'),
]