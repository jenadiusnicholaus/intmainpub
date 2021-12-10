from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, User
)
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):
    image = models.FileField(upload_to='profile_files', null=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=20, null=True)
    profession = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(max_length=300, null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    facebook_link = models.URLField(max_length=400, null=True, blank=True)
    linkedin_link = models.URLField(max_length=400, null=True, blank=True)
    tweeter_link = models.URLField(max_length=400, null=True, blank=True)
    github_link = models.URLField(max_length=400, null=True, blank=True)
    followers = models.ManyToManyField(
        User, symmetrical=False, related_name='followers', blank=True,)
    following = models.ManyToManyField(
        User, symmetrical=False, related_name='following', blank=True,)

    class Meta:

        verbose_name_plural = 'User Profile'

    def __str__(self):
        return str(self.user.username)

    def imageUrl(self):
        if self.image:
            return self.image.url
        return None

    def get_fullname(self):
        if not self.user.first_name and not self.user.last_name:
            return self.user.username
        else:
            full_name = f'{self.user.first_name} {self.user.last_name} '
            return full_name

    def getfirstChar(self):
        if not self.user.first_name and not self.user.last_name:
            return self.user.username[0]
        else:
            full_name = f'{self.user.first_name} {self.user.last_name} '
            return self.user.first_name[0]


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=User)
