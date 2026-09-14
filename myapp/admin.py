from django.contrib import admin
from .models import Category, Channel, Video, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    search_fields = ('name', 'user__username')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'channel', 'category', 'views', 'likes', 'created_at')
    list_filter = ('category', 'created_at') 
    search_fields = ('title', 'description')  
    list_editable = ('category',)            


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'video', 'created_at')
    search_fields = ('text', 'user__username', 'video__title')