from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email, password=None, username=None, **extra_fields):
        """Create and return a `User` with an email and password."""
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.username = username
        user.set_password(password)
        user.is_activate = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, username=username,
                                password=password, **extra_fields)
        user.username = username
        user.email = email
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, ):
    firstname = models.CharField(max_length=30, null=True)
    middlename = models.CharField(max_length=30, null=True)
    lastname = models.CharField(max_length=30, null=True)
    username = models.CharField(
        max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        if self.username:
            return str(self.username)
        return str(self.email)

    def get_username(self):
        return str(self.username)

    def get_fullname(self):
        if not self.firstname and not self.lastname:
            return str(self.username)
        return f'{self.firstname} {self.lastname}'

    def getfirstChar(self):
        if self.username:
            return str(self.username[0])
        return str(self.email[0])


class UserProfile(models.Model):
    image = models.FileField(upload_to='profile_files', null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=20, null=True)
    profession = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(max_length=300, null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    facebook_link = models.URLField(max_length=400, null=True, blank=True)
    linkedin_link = models.URLField(max_length=400, null=True, blank=True)
    tweeter_link = models.URLField(max_length=400, null=True, blank=True)
    github_link = models.URLField(max_length=400, null=True, blank=True)

    def __str__(self):
        return str(self.user.email)

    def imageUrl(self):
        if self.image:
            return self.image.url
        return None


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
