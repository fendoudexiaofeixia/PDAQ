from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.urls import reverse
from xadmin.filters import RelatedFieldListFilter, manager

from my_app.adminforms import PdaqAdminForm
from my_app.base_admin import BaseOwnerAdmin
from .models import Category, Pdaq, Custom
import xadmin


class PdaqInline(BaseOwnerAdmin):
    fields = ('ip', 'desc')
    extra = 0
    model = Pdaq


# Register your models here.
@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ['name', 'status', 'is_nav', 'owner', 'create_time']
    fields = ('name', 'status', 'is_nav', 'owner')
    inlines = [PdaqInline, ]


@xadmin.sites.register(Custom)
class CustomAdmin(BaseOwnerAdmin):
    list_display = ['name', 'owner', 'create_time']
    fields = ['name', 'owner']


@xadmin.sites.register(Pdaq)
class PdaqAdmin(BaseOwnerAdmin):
    list_per_page = 10
    form = PdaqAdminForm
    list_display = ['ip', 'custom_ip', 'MODEL', 'ICCID', 'Set_meal', 'USB', 'comm', 'GPS', 'SD', 'INTERNET',
                    'serial_number',
                    'create_time',
                    'category', 'custom', 'owner', 'status']
    list_filter = ['category', 'custom']
    list_display_links = []
    actions_on_top = True
    search_fields = [
        'ip',
    ]
    exclude = ('owner',)
    fieldsets = (
        ('基础信息', {
            'description': '基础信息描述',
            'fields': (
                'ip', 'custom_ip', 'MODEL', 'category', 'ICCID', 'serial_number', 'Set_meal', 'custom', 'status'
            ),

        }),
        ('摘要信息', {
            'classes': ('collapse',),
            'fields': ('desc',),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('USB', 'comm', 'GPS', 'SD', 'INTERNET')
        }),
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}"><a/>',
            reverse('admin_my_app_pdaq_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    # def get_queryset(self, request):
    #     qs = super(PdaqAdmin, self).get_queryset(request)
    # return qs.filter(owner=request.user)
    # return qs
    # if request.user.is_superuser:
    #     return qs
    # else:
    #     return qs.filter(owner=request.user)


class CategoryOwnerFilter(RelatedFieldListFilter):
    """自定义过滤器，只展示当前用户分类"""

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')
        # print('*********************************', Category.objects.filter().values_list('id', 'name'))


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(LogEntry)
class LogEntryAdmin(BaseOwnerAdmin):
    list_display = ['object_id', 'action_flag', 'user', 'change_message']


xadmin.sites.site_title = 'PDAQ后台管理'
xadmin.sites.index_title = '信息管理'
xadmin.sites.site_header = 'PDAQ信息管理系统'
