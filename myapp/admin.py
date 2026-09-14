from django.contrib import admin
from .models import Category, Channel, Video, Comment


# Настройка отображения категорий
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Автоматически заполняет slug из названия
    search_fields = ('name',)


# Настройка отображения каналов
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    search_fields = ('name', 'user__username')


# Настройка отображения видео
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'channel', 'category', 'views', 'likes', 'created_at')
    list_filter = ('category', 'created_at')  # Фильтры в правой колонке админки
    search_fields = ('title', 'description')   # Поиск в админке по заголовку и описанию
    list_editable = ('category',)             # Возможность менять категорию прямо из списка


# Настройка отображения комментариев
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'video', 'created_at')
    search_fields = ('text', 'user__username', 'video__title')