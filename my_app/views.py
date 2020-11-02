from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file
# Create your views here.
from my_app.models import Pdaq, Custom, Category


def pdaq_list(request, category_id=None, custom_id=None):
    category = []
    custom = []
    if custom_id:
        p_list, custom = Pdaq.get_by_custom(custom_id)
    elif category_id:
        p_list, category = Pdaq.get_by_category(category_id)
    else:
        p_list = Pdaq.latest_pdaqs()
        # custom = Custom.get_customs()
    context = {
        'category': category,
        'custom': custom,
        'p_list': p_list,
    }
    # print(context)
    context.update(Category.get_navs())
    context.update(Custom.get_customs())
    return render(request, 'list.html', context=context)


def pdaq_detail(request, serial_number):
    try:
        pdaq = Pdaq.objects.get(serial_number=serial_number)
        # print(pdaq)
    except Pdaq.DoesNotExist:
        pdaq = None
    context = {
        'pdaq': pdaq
    }
    context.update(Category.get_navs())
    context.update(Custom.get_customs())
    return render(request, 'detail.html', context=context)


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})
