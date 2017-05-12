from ajax_select import register, LookupChannel
from django.contrib.auth.models import User

from portal.models import Category


@register('user')
class UserLookup(LookupChannel):
    model = User

    def get_query(self, q, request):
        return self.model.objects.filter(username__icontains=q).order_by('username')


@register('categories')
class CategoryLookup(LookupChannel):
    model = Category

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')