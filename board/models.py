from django.conf import settings
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='advertisements')
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Response by {self.author} to "{self.advertisement}"'
