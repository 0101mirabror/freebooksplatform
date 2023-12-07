from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class CustomUser(AbstractUser):
   email = models.EmailField(unique=True)
   username = models.CharField(max_length=20, unique=True)
   firstname = models.CharField(max_length=20)
   lastname = models.CharField(max_length=20)
   image = models.ImageField(upload_to="media/profile_pictures", default="author_images/profile.png",null=True, blank=True)
   # slug = models.SlugField()
   # def save(self, *args, **kwargs):
   #     if not self.slug:
   #         self.slug = slugify(self.title)
   #     super(CustomUser, self).save(*args, **kwargs)
 

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    