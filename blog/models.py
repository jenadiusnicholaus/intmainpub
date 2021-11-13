from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
# Create your models here.
from django.utils import timezone
from django.utils.text import slugify
from intmainblog import settings

from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from six import python_2_unicode_compatible
import uuid

STATUS = (
    (0, 'Draft'),
    (1, 'Published')
)

COLOR = (
    ('primary', 'primary'),
    ('warning', "warning"),
    ('success', "success"),
    ('danger', "danger"),
    ('info', "info"),

)

User = settings.AUTH_USER_MODEL


class Topics(models.Model):
    title = models.CharField(max_length=300, null=False, blank=False)
    image = models.FileField(blank=True, null=True, upload_to='Pub_files')
    color = models.CharField(max_length=25, choices=COLOR)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Topics'

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Publication(models.Model):
    topic = models.ForeignKey(Topics, on_delete=models.SET_NULL,
                              related_name='publication', null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='blog_posts', null=True)
    title = models.CharField(max_length=300, null=False, blank=False)
    slug = models.SlugField(max_length=1000, unique=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to='Pub_files')
    short_description = models.TextField(blank=True, null=True)
    description = RichTextUploadingField(null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS, default=0)
    bitBucket_link = models.URLField(max_length=400, null=True, blank=True)
    docker_link = models.URLField(max_length=400, null=True, blank=True)
    gitlab_link = models.URLField(max_length=400, null=True, blank=True)
    github_link = models.URLField(max_length=400, null=True, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Publication, self).save(*args, **kwargs)

    def getFullname(self):
        return f'{self.author.firstname}  .  {self.author.middlename[0]} . {self.author.lastname}'


class PublicationComment(models.Model):
    content = models.TextField(max_length=1000, null=True, blank=True)
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='pub_commenter')
    publication = models.ForeignKey(
        Publication, on_delete=models.SET_NULL, null=True,  related_name='commented_pub')
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = ' publication comments'

    def __str__(self):
        return str(self.commenter.username)
