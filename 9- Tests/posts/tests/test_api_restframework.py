from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework.test import APIRequestFactory, force_authenticate

from posts.api.views import (
    PostCreateAPIView,
    PostDeleteAPIView,
    PostDetailAPIView,
    PostListAPIView,
    PostUpdateAPIView,
)

from posts.models import Post

User = get_user_model()


class PostAPITestCase(TestCase):
    def setUp(self):
        self.data = {"title": "new titile",
                     "content": "new content", "publish": timezone.now().date()}
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username='tester',
            email='tester@gmail.com',
            password='testerpw',
            is_staff=True,
            is_superuser=True,
        )

    def create_post(self, title="new title"):
        return Post.objects.create(title=title)

    def test_get_data(self):
        list_url = reverse("posts-api:list")
        obj = self.create_post()
        detail_url = reverse("posts-api:detail", kwargs={"slug": obj.slug})

        request = self.factory.get(list_url)
        respones = PostListAPIView.as_view()(request)
        self.assertEqual(respones.status_code, 200)

        request_ = self.factory.get(detail_url)
        respones_ = PostListAPIView.as_view()(request, slug=obj.slug)
        self.assertEqual(respones_.status_code, 200)

    def test_post_data(self):
        create_url = reverse("posts-api:create")
        request = self.factory.post(create_url, data=self.data)
        response1 = PostCreateAPIView.as_view()(request)
        self.assertEqual(response1.status_code, 401)

        force_authenticate(request, user=self.user)
        response2 = PostCreateAPIView.as_view()(request)
        self.assertEqual(response2.status_code, 201)

    def test_update_data(self):
        obj = self.create_post()
        update_url = reverse("posts-api:update", kwargs={"slug": obj.slug})
        request = self.factory.put(update_url, data=self.data)
        response1 = PostUpdateAPIView.as_view()(request, slug=obj.slug)
        self.assertEqual(response1.status_code, 401)

        force_authenticate(request, user=self.user)
        response2 = PostUpdateAPIView.as_view()(request, slug=obj.slug)
        self.assertEqual(response2.status_code, 200)

    def test_delete_data(self):
        obj = self.create_post(title='another new title')
        delete_url = reverse("posts-api:delete", kwargs={"slug": obj.slug})
        request = self.factory.delete(delete_url)
        response1 = PostDeleteAPIView.as_view()(request, slug=obj.slug)
        self.assertEqual(response1.status_code, 401)

        force_authenticate(request, user=self.user)
        response2 = PostDeleteAPIView.as_view()(request, slug=obj.slug)
        self.assertEqual(response2.status_code, 204)
