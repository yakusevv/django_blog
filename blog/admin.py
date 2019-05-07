from django.contrib import admin
from django.db.models import Count
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Post, Tag, Profile


admin.site.unregister(User)


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


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
