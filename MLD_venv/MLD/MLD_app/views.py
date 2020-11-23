from django.shortcuts import render
from rest_framework.decorators import api_view
from MLD import settings
from MLD_app import py_model
import os


# Create your views here.


def class_view(request):
    context = {
        'class_data': py_model.Dropdwn_class()
    }

    return render(request, 'home.html', context=context)


@api_view(['GET'])
def frames_display(request, value):
    a = py_model.selectedimg(value)
    path = settings.MEDIA_ROOT
    img_list = os.listdir(path + '\\' + value) if value == "laptop" or value == 'person' else []
    context = {
        'user_val': value,
        'images': img_list,
        'media_url': settings.MEDIA_URL
    }
    print()

    return render(request, 'view_images.html', context=context)
