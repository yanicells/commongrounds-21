from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    model = Post


class CommentAdmin(admin.ModelAdmin):
    model = Comment


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
