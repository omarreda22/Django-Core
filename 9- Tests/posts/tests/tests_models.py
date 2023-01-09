from django.test import TestCase

from posts.models import Post


"""
    1- setUp data using actully model in def setup
    2- test fake data
    3- to def will be test method must to begin with "test"
    .. what you want to test [ 'title' - 'slug' ]
"""


class PostModelTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title='A new title', slug='a-new-title')

    def create_post(self, title="new title"):
        return Post.objects.create(title=title)

    def test_post_title(self):
        obj = Post.objects.get(slug='a-new-title')
        self.assertEqual(obj.title, 'A new title')

    def test_post_slug(self):
        title1 = 'title abc'
        obj1 = self.create_post(title=title1)
        obj2 = self.create_post(title=title1)
        obj3 = self.create_post(title=title1)
        # slug
        qs = Post.objects.filter(title=title1)
        self.assertEqual(qs.count(), 3)
        # unique slug
        qs = Post.objects.filter(slug=obj1.slug)
        self.assertEqual(qs.count(), 1)
