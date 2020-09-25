from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    def __str__(self):
        return self.name

    STAUTS_NORMAL = 1
    STATUS_DIFF = 0
    STATUS_ITEMS = {
        (STAUTS_NORMAL, '正常'),
        (STATUS_DIFF, '删除'),
    }
    name = models.CharField(max_length=128, verbose_name='名称')
    status = models.PositiveIntegerField(default=STAUTS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='创建者', on_delete=models.PROTECT, db_constraint=False, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    @classmethod
    def get_navs(cls):
        nav_categories = []
        normal_categories = []
        categories = cls.objects.filter(status=cls.STAUTS_NORMAL)
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        # nav_categories = categories.filter(is_nav=True)
        # normal_categories = categories.filter(is_nav=False)
        # print(normal_categories)
        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }


class Custom(models.Model):
    def __str__(self):
        return self.name

    STATUS_NORMAL = 1
    STATUS_DIFF = 0
    STATUS_ITEMS = {
        (STATUS_NORMAL, '正常'),
        (STATUS_DIFF, '完结'),
    }
    name = models.CharField(max_length=128, verbose_name='客户')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='客户状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    owner = models.ForeignKey(User, verbose_name='创建者', on_delete=models.PROTECT, db_constraint=False, null=True)

    class Meta:
        verbose_name_plural = verbose_name = '客户'

    @classmethod
    def get_customs(cls):
        cus = []
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        for custom in queryset:
            cus.append(custom)
        # print(cus,queryset)
        return {
            'customs': queryset,
        }


class Pdaq(models.Model):
    def __str__(self):
        return self.ip

    STATUS_NORMAL = 1
    STATUS_DIFF = 0
    STATUS_DEMAGE = 2
    STATUS_ITEMS = {
        (STATUS_NORMAL, '正常'),
        (STATUS_DIFF, '维修'),
        (STATUS_DEMAGE, '损坏'),
    }
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='设备状态')
    ip = models.CharField(max_length=50, primary_key=True, verbose_name='IP地址')
    custom_ip = models.CharField(max_length=50, verbose_name='客户IP', blank=True, null=True)
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    ICCID = models.CharField(max_length=128, verbose_name='ICCID')
    Set_meal = models.CharField(max_length=50, verbose_name='流量卡套餐', null=False, blank=False, default='48G/年')
    USB = models.CharField(max_length=128, verbose_name='USB速率')
    comm = models.CharField(max_length=128, verbose_name='4G速率')
    GPS = models.CharField(max_length=128, verbose_name='GPS速率')
    serial_number = models.CharField(max_length=128, verbose_name='序列号')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.PROTECT, db_constraint=False)
    custom = models.ForeignKey(Custom, verbose_name='客户', on_delete=models.PROTECT, db_constraint=False)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='创建者', db_constraint=False, null=False,
                              blank=False)

    class Meta:
        verbose_name_plural = verbose_name = 'pdaq'

    @staticmethod
    def get_by_custom(custom_id):
        try:
            custom = Custom.objects.get(id=custom_id)
        except Custom.DoesNotExist:
            custom = None
            p_list = []
        else:
            p_list = custom.pdaq_set.filter(category=Category.STAUTS_NORMAL).select_related('owner')
        return p_list, custom

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            p_list = []
        else:
            p_list = category.pdaq_set.filter(status=Category.STAUTS_NORMAL).select_related('owner')
        return p_list, category

    @classmethod
    def latest_pdaqs(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        # print(queryset)
        return queryset
