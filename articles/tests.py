from django.test import TestCase
from rest_framework.reverse import reverse
import json

from api.tests import BaseAPITest
from mixer.backend.django import mixer

from articles.models import Category, Article
from hospitals.models import Hospital


class TestArticleApiView(BaseAPITest):
    def setUp(self):
        self.hospital = mixer.blend(Hospital)
        # self.user = self.create_and_login()
        self.user = self.create_and_login(email="test2@test.com", hospital=self.hospital, is_writer=True)
        self.category = mixer.blend(Category)
        self.article = mixer.blend(Article, author=self.user, category=self.category, hospital=self.user.hospital)

        class mydict(dict):
            def __str__(self):
                return json.dumps(self)

        couples = [['title', 'Test'],
                   ['text', 'test'],
                   ['excerpt', 'test'],
                   ['category_id', self.category.id]]

        self.create_data = mydict(couples)

    def test_list(self):
        # resp = self.client.get('/v1/articles/', )
        resp = self.client.get(reverse('v1:articles:articles-list'))
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(resp.data), Article.objects.all().count())

    def test_detail_article(self):
        # resp = self.client.get('/v1/articles/1/', )
        resp = self.client.get(reverse('v1:articles:articles-detail', args=(self.article.pk,)))
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        resp = self.client.post('/v1/articles/', data=self.create_data, content_type='application/json')
        # resp = self.client.post(reverse('v1:articles:articles-list'), data=self.create_data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['title'], self.create_data['title'])
        self.assertEqual(resp.data['excerpt'], self.create_data['excerpt'])
        self.assertEqual(resp.data['text'], self.create_data['text'])

        obj = Article.objects.get(title=self.create_data['title'], author=self.user)
        self.assertEqual(obj.text, self.create_data['text'])
        self.assertEqual(obj.category, self.category)
