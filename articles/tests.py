from django.test import TestCase
from rest_framework.reverse import reverse

from api.tests import BaseAPITest
from mixer.backend.django import mixer

from articles.models import Category, Article
from hospitals.models import Hospital


class TestArticleApiView(BaseAPITest):
    def setUp(self):
        self.hospital = mixer.blend(Hospital)
        self.user = self.create_and_login(hospital=self.hospital, is_writer=True)
        self.category = mixer.blend(Category)
        self.article = mixer.blend(Article, author=self.user, category=self.category, hospital=self.user.hospital)

        self.create_data = {
            "title": "Test",
            "excerpt": "Test",
            "text": "Test",
            "category_id": self.category.id
        }
        self.update_data = {
            "title": "Updated test",
            "excerpt": "Updated test",
            "text": "Updated test",
            "category_id": self.category.id
        }
        self.partial_data = {
            "title": "Partial test",
            "text": "Partial test",
        }

    def test_list(self):
        resp = self.client.get(reverse('v1:articles:articles-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['results']), Article.objects.filter(hospital=self.user.hospital).count())

    def test_detail_article(self):
        resp = self.client.get(reverse('v1:articles:articles-detail', args=(self.article.id,)))
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        resp = self.client.post(reverse('v1:articles:articles-list'), data=self.create_data, )

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['title'], self.create_data['title'])
        self.assertEqual(resp.data['excerpt'], self.create_data['excerpt'])
        self.assertEqual(resp.data['text'], self.create_data['text'])

        obj = Article.objects.get(title=self.create_data['title'], author=self.user)
        self.assertEqual(obj.text, self.create_data['text'])
        self.assertEqual(obj.category, self.category)

    def test_update(self):
        resp = self.client.put(reverse('v1:articles:articles-detail', args=(self.article.id,)),
                               data=self.update_data, )
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.data['title'], self.update_data['title'])
        self.assertEqual(resp.data['excerpt'], self.update_data['excerpt'])
        self.assertEqual(resp.data['text'], self.update_data['text'])
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, self.update_data['title'])
        self.assertEqual(self.article.excerpt, self.update_data['excerpt'])
        self.assertEqual(self.article.text, self.update_data['text'])

    def test_partial_update(self):
        resp = self.client.patch(reverse('v1:articles:articles-detail', args=(self.article.id,)),
                                 data=self.partial_data, )
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.data['title'], self.partial_data['title'])
        self.assertEqual(resp.data['excerpt'], self.article.excerpt)
        self.assertEqual(resp.data['text'], self.partial_data['text'])
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, self.partial_data['title'])
        self.assertEqual(self.article.text, self.partial_data['text'])

    def test_delete(self):
        resp = self.client.delete(reverse('v1:articles:articles-detail', args=(self.article.id,)))
        self.assertEqual(resp.status_code, 204)

    def test_update_not_author(self):
        self.user2 = self.create(email='wrong_author@mail.com')
        self.article.author = self.user2
        self.article.save()

        resp = self.client.put(reverse('v1:articles:articles-detail', args=(self.article.id,)),
                               data=self.update_data, )
        self.assertEqual(resp.status_code, 403)

    def test_non_authenticated(self):
        self.logout()
        resp = self.client.get(reverse('v1:articles:articles-list'))

        self.assertEqual(resp.status_code, 401)

