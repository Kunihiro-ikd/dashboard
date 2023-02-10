from django.shortcuts import render
from .forms import UploadForm
from .models import UploadImage
# Create your views here.

def upload_img(request):
    template_name = 'upload_img.html'
    context = {
        'title': '画像のアップロード',
        'upload_form': UploadForm(),
        'id': None,
    }

    if (request.method == 'POST'):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_image = form.save()

            context['id'] = upload_image.id
    return render(request, template_name, context)