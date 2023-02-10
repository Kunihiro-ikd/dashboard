from django.db import models


def savePath(instance, filename):
    ext = filename.split('.')[-1]
    new_name = instance.title + "_saved"
    return f'files/{new_name}.{ext}'

# Create your models here.
class UploadImage(models.Model):
    title = models.CharField(max_length=100, default="nanashi")
    image = models.ImageField(upload_to=savePath)

    def __str__(self):
        return self.title

