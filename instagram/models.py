from django.db import models
from django.contrib.auth.models import User
from PIL import Image as pil_img
import datetime
from django.utils import timezone
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    profile_photo = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    bio = models.TextField(blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        
    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        profile = Profile.objects.filter(user__username__icontains = name)
        return profile

    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    image_name = models.CharField(max_length=20, blank=True)
    image_caption = models.CharField(max_length=100)
    likes = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, default='1')

    def __str__(self):
        return self.image_caption

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    
    @classmethod
    def update_caption(cls, update):
        pass
    
    @classmethod
    def get_image_id(cls, id):
        image = Image.objects.get(pk=id)
        return image
    
    @classmethod
    def get_profile_images(cls, profile):
        images = Image.objects.filter(profile__pk = profile)
        return images
    
    @classmethod
    def get_all_images(cls):
        images = Image.objects.all()
        return images

    class Meta:
        ordering = ['-date_posted']    


class Comment(models.Model):
    comment = HTMLField()
    posted_on = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_comment(self):
        self.save()
    
    def save_comment(self):
        self.save()
    
    @classmethod
    def get_comments_by_images(cls, id):
        comments = Comment.objects.filter(image__pk = id)
        return comments