from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.has_perm('news.add_post')

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('news.change_post')

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('news.delete_post')

admin.site.register(Post, PostAdmin)