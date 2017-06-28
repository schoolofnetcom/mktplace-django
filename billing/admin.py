from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from django.contrib import admin

# Register your models here.
from billing.models import Order


class OrderAdmin(AjaxSelectAdmin):
    list_filter = ['status', 'created_at']
    list_display = ('id', 'user','merchant', 'commission', 'total', 'status')
    form = make_ajax_form(Order, {
        'user':'user',
    })

admin.site.register(Order, OrderAdmin)