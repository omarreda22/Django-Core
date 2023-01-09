from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from posts.models import Post
from posts.views import post_update, post_create

User = get_user_model()


class PostViewAuthTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username='tester',
            email='tester@gmail.com',
            password='testerpw',
            is_staff=True,
            is_superuser=True,
        )

    def create_post(self, title="new title"):
        return Post.objects.create(title=title)

    def test_user_update_with_auth(self):
        obj = self.create_post(title='new title for test-user-atuh')
        # request factory to processing the reuqest as commit = false
        request = self.factory.get(obj.get_absolute_url() + 'edit/')
        request.user = self.user
        response = post_update(request, slug=obj.slug)
        self.assertEqual(response.status_code, 200)

    # create post
    def test_user_create_new_post(self):
        obj = self.create_post(title='create post')
        request = self.factory.post('/posts/create/')
        request.user = self.user
        reponse = post_create(request)
        self.assertEqual(reponse.status_code, 200)

    def test_update_view(self):
        obj = self.create_post(title='new title for view test')
        # edit_url = reverse("posts:update", kwargs={"slug":obj.slug})
        response = self.client.get(obj.get_absolute_url() + 'edit/')
        # print(response.status_code)
        self.assertEqual(response.status_code, 404)

    def test_delete_view(self):
        obj = self.create_post(title='new title for view test')
        # delete_url = reverse("posts:delete", kwargs={"slug":obj.slug})
        response = self.client.get(obj.get_absolute_url() + 'delete/')
        # print(response.status_code)
        self.assertEqual(response.status_code, 404)
