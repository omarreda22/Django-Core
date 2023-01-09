from django.test import TestCase
from django.utils import timezone

from posts.models import Post
from posts.forms import PostForm


class PostFormTestCase(TestCase):
    def test_valid_form(self):
        title = 'A new title'
        slug = 'new-title-for-test-forms'
        content = 'this our content'
        obj = Post.objects.create(
            title=title, slug=slug, publish=timezone.now(), content=content)
        data = {'title': obj.title, 'slug': obj.slug,
                'publish': obj.publish, 'content': obj.content}
        form = PostForm(data=data)  # PostForm(reuqest.POST)
        # print(form.errors)
        self.assertTrue(form.is_valid())
        """ 
            to write form.cleand_data must write is_valid
            because is_valid grabed cleand_data method
        """
        self.assertEqual(form.cleaned_data.get('title'), obj.title)
        self.assertNotEqual(form.cleaned_data.get('content'), 'wrong content')

    def test_invalid_form(self):
        title = 'A new title'
        slug = 'new-title-for-test-forms'
        content = 'this our content'
        obj = Post.objects.create(
            title=title, slug=slug, publish=timezone.now(), content=content)
        data = {'title': obj.title, 'slug': obj.slug,
                'publish': obj.publish, 'content': ""}
        form = PostForm(data=data)
        self.assertFalse(form.is_valid())
        # print(form.errors)
        self.assertTrue(form.errors)
