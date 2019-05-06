from django.contrib import admin
from django.db.models import Count

from .models import Post, Tag, Profile
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'shorted_body', 'display_tags', 'date_pub')
    list_filter = ('date_pub', 'tags')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'number_of_posts')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _number_of_posts=Count("posts")
            )
        return queryset

    def number_of_posts(self, obj):
        return obj._number_of_posts

    number_of_posts.admin_order_field = '_number_of_posts'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
     pass
