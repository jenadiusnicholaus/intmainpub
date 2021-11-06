from ckeditor.fields import RichTextField

from django.db import models

# Create your models here.
from django.utils import timezone

STATUS = (
    (0, 'Draft'),
    (1, 'Published')
)
from intmainblog import settings

User = settings.AUTH_USER_MODEL


class Publication(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=300, null=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to='Pub_files')
    short_description = models.TextField(blank=True, null=True)
    description = RichTextField(null=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def getFullname(self):
        return f'{self.author.firstname}  .  {self.author.middlename[0]} . {self.author.lastname}'


