from django.db import models
from django.utils import timezone
from datetime import datetime, date
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

################################### EMAIL ###################################
class ContactForm(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username




################################### BLOG ###################################
# class Author(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_picture = models.ImageField()

#     def __str__(self):
#         return self.user.username


# class Category(models.Model):
#     title = models.CharField(max_length=20)

#     def __str__(self):
#         return self.title


# class Post(models.Model):
#     title = models.CharField(max_length=100)
#     overview = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     content = RichTextField(default=False)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     thumbnail = models.ImageField()
#     categories = models.ManyToManyField(Category)
#     featured = models.BooleanField()

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse('post-detail', kwargs={
#             'pk': self.pk
#         })

#     def get_update_url(self):
#         return reverse('post-update', kwargs={
#             'pk': self.pk
#         })

#     def get_delete_url(self):
#         return reverse('post-delete', kwargs={
#             'pk': self.pk
#         })

     


