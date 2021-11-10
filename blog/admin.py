from django.contrib import admin
from .models import *


# Register your models here.

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Publication, PublicationAdmin)
admin.site.register(Topics, )
admin.site.register(PublicationComment)
