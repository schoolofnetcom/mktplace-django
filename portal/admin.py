from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from portal.models import Category, Product, ProductAnswer, ProductQuestion, UserProfile, ProductImages


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


class CategoryAdmin(AjaxSelectAdmin):
    prepopulated_fields = {"slug": ('name',)}
    list_filter = ['hidden']
    list_display = ('id', 'name', 'parent', 'hidden')
    form = make_ajax_form(Category, {
        'parent': 'categories',
    })


class ProductImageInline(admin.StackedInline):
    model = ProductImages

class ProductAdmin(AjaxSelectAdmin):
    prepopulated_fields = {"slug": ('name',)}
    list_filter = ['status']
    list_display = ('id', 'name', 'short_description', 'status')
    inlines = (ProductImageInline, )
    form = make_ajax_form(Product, {
        'user': 'user',
        # 'categories': 'categories'
    })


class ProductAnswerInline(admin.StackedInline):
    model = ProductAnswer
    can_delete = False


class ProductQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'question', 'status')
    inlines = (ProductAnswerInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductQuestion, ProductQuestionAdmin)
