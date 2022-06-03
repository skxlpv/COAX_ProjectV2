from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from rest_framework import serializers

from articles import models

admin.site.register(models.Categories)


@admin.register(models.Articles)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ('id', 'status', 'title', 'excerpt', 'text', 'category', 'author',)
