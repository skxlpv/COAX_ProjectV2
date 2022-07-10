from django.contrib import admin

from articles import models

admin.site.register(models.Category)


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'title', 'excerpt', 'text', 'category', 'author',)
