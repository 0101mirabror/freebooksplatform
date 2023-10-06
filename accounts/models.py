from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class CustomUser(AbstractUser):
   email = models.EmailField(unique=True)
   username = models.CharField(max_length=20, unique=True)
   firstname = models.CharField(max_length=20)
   lastname = models.CharField(max_length=20)
   image = models.ImageField(upload_to="media/profile_pictures", null=True, blank=True)
   # slug = models.SlugField()
   # def save(self, *args, **kwargs):
   #     if not self.slug:
   #         self.slug = slugify(self.title)
   #     super(CustomUser, self).save(*args, **kwargs)
 