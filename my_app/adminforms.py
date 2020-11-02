from django import forms

# from django.contrib.admin.views import autocomplete

from my_app.models import Category, Custom
# from dal import autocomplete


class PdaqAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    # category = forms.ModelChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='category-autocomplete'),
    #     label='分类',
    # )
    # custom = forms.ModelMultipleChoiceField(
    #     queryset=Custom.objects.all(),
    #     widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
    #     label='标签',
    # )
