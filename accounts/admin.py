from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Post

def create_authors_group():
    authors_group, created = Group.objects.get_or_create(name='authors')
    if created:
        content_type = ContentType.objects.get_for_model(Post)
        permissions = Permission.objects.filter(content_type=content_type)
        authors_group.permissions.set(permissions)
        authors_group.save()

class GroupAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.name == 'authors':
            create_authors_group()

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

create_authors_group()