from django.shortcuts import render, redirect
from .forms import UploadForm
from .models import UploadImage
import cv2
from django.conf import settings
import os
import logging
from .models import Document
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
from .image_generator.def_nueral_style import NueralStyle

# Create your views here.
logger = logging.getLogger('development')
# logger.info('a-----------')

# def aaa_upload_img(request, num):
#     template_name = 'upload_img.html'
#     context = {
#         'title': '画像のアップロード',
#         'upload_form': UploadForm(),
#         'id': None,
#     }

#     if (request.method == 'POST'):
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
            
#             upload_image = form.save()
#             print('b---------------')

#             context['id'] = upload_image.id
#             print(context)
#     return render(request, template_name, context)

def gray(url):
    img = cv2.imread(url)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output_path = "media/gallery"

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    cv2.imwrite(output_path / "gray.jpg", img_gray)

# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
# def simple_upload(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         return render(request, 'core/simple_upload.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'core/simple_upload.html')


def img_upload(request):
    template_name = 'upload_img.html'
    uploaded_file_url = ''
    gray_path = ''

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # ファイルの保存
            form.save()
            upload_img_file = request.FILES['document']
            fs = FileSystemStorage()
            filename = fs.save(upload_img_file.name, upload_img_file)
            uploaded_file_url = fs.url(filename)

            # views.py ではルートパスだと画像が読み込めないため、/を消す
            uploaded_file_url = uploaded_file_url[1:]

            # 拡張子の前で区切るため添字の取得
            target ='.'
            idx = uploaded_file_url.find(target)

            # 灰色の画像を保存するパスの作成と保存
            gray_path = uploaded_file_url[:idx]+'_gray'+uploaded_file_url[idx:]
            transform_gray(uploaded_file_url, gray_path)

            # html では / がついていないと画像が読み込めないため/をつけて渡す
            uploaded_file_url = '/' + uploaded_file_url
            gray_path = '/' + gray_path
    else:
        form = DocumentForm()
    
    data = {
        'form': form, 
        'uploaded_file_url': uploaded_file_url,
        'gray_path': gray_path,
    }

    return render(request, template_name, data)


def transform_gray(uploaded_file_url, gray_path):
    style_change_image = cv2.imread(uploaded_file_url)
    style_change_image = cv2.cvtColor(style_change_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(gray_path, style_change_image)
    

def nueral_style(request):
    template_name = 'nueral_style_transform.html'
    form = DocumentForm(request.POST, request.FILES)
    transform_path = ''
    uploaded_file_url = ''

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            print("valid")
            
             # ファイルの保存
            form.save()
            upload_img_file = request.FILES['document']
            fs = FileSystemStorage()
            filename = fs.save(upload_img_file.name, upload_img_file)
            uploaded_file_url = fs.url(filename)

            # views.py ではルートパスだと画像が読み込めないため、/を消す
            uploaded_file_url = uploaded_file_url[1:]

            # 拡張子の前で区切るため添字の取得
            target ='.'
            idx = uploaded_file_url.find(target)

            # 灰色の画像を保存するパスの作成と保存
            print("uploaded_file_url", uploaded_file_url)
            transform_path = uploaded_file_url[:idx]+'_transform'
            print("transform_path", transform_path)

            # ゴッホの画像の画像の指定
            STYLE_PATH = "media/cnn/1-style-gogh.jpg"

            nueral_style = NueralStyle(uploaded_file_url, STYLE_PATH, transform_path)
            nueral_style.stylize()
            # html に渡す時はrootにする
            uploaded_file_url = '/' + uploaded_file_url
            transform_path= transform_path + uploaded_file_url[idx+1:]
            transform_path = '/' + transform_path



    data = {
        'form': form, 
        'uploaded_file_url': uploaded_file_url,
        'transform_path': transform_path
    }

    return render(request, template_name, data)



    
# def img_upload(request):
#     print('---------')
#     print(request.FILES)
#     print('---------')

#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         return render(request, 'upload_img.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'upload_img.html')