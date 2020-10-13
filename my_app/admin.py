from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.urls import reverse

from my_app.adminforms import PdaqAdminForm
from my_app.base_admin import BaseOwnerAdmin
from .models import Category, Pdaq, Custom


class PdaqInline(admin.TabularInline):
    fields = ('ip', 'desc')
    extra = 0
    model = Pdaq


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'is_nav', 'owner', 'create_time']
    fields = ('name', 'status', 'is_nav', 'owner')
    inlines = [PdaqInline, ]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Custom)
class CustomAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'create_time']
    fields = ['name', 'owner']

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CustomAdmin, self).save_model(request, obj, form, change)


@admin.register(Pdaq)
class PdaqAdmin(admin.ModelAdmin):
    form = PdaqAdminForm
    list_display = ['ip', 'custom_ip', 'MODEL', 'ICCID', 'Set_meal', 'USB', 'comm', 'GPS', 'SD', 'INTERNET',
                    'serial_number',
                    'create_time',
                    'category', 'custom', 'owner', 'status']
    list_filter = ['category', 'custom']
    list_display_links = []
    actions_on_top = True
    search_fields = [
        'category', 'custom'
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

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PdaqAdmin, self).save_model(request, obj, form, change)

    def operator(self, obj):
        return format_html(
            '<a href="{}"><a/>',
            reverse('admin_my_app_pdaq_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def get_queryset(self, request):
        qs = super(PdaqAdmin, self).get_queryset(request)
        # return qs.filter(owner=request.user)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PdaqAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器，只展示当前用户分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values.list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_id', 'action_flag', 'user', 'change_message']


admin.site.site_title = 'PDAQ后台管理'
admin.site.index_title = '信息管理'
admin.site.site_header = 'PDAQ信息管理系统'
