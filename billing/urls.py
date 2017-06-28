from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^payment/product/(?P<product_id>[\d]+$)', views.payment, name='billing_payment'),
    url(r'^purchased/(?P<order_id>[\d]+$)', views.item_purchased, name='billing_item_purchased'),
    url(r'^sales/order/edit/(?P<order_id>[\d]+$)', views.change_shipment_status, name='billing_change_shipment_status'),
    url(r'^sales$', views.sales, name='billing_sales'),
    url(r'^my_orders$', views.my_orders, name='billing_my_orders')
]
