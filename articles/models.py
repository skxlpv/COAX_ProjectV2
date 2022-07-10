from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from hospitals.models import Hospital
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = _('Category')

    def __str__(self):
        return self.name


class Article(models.Model):
    class ArticleObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    REVIEW = 'RW'
    PUBLISHED = 'PB'
    options = (
        (REVIEW, 'On review'),
        (PUBLISHED, 'Published'),
    )

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=250)
    excerpt = models.TextField()
    text = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default='')
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, default=''
    )
    status = models.CharField(
        max_length=10, choices=options, default='review')
    objects = models.Manager()
    postobjects = ArticleObjects()

    class Meta:
        verbose_name_plural = _('Articles')
        verbose_name = _('Article')
        ordering = ('-published',)

    def __str__(self):
        return self.title
