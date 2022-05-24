from django.contrib import admin

from articles import models

admin.site.register(models.Articles)
# admin.site.register(models.Categories)
# @admin.register(models.Articles)
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'excerpt', 'text', 'author', 'published')
