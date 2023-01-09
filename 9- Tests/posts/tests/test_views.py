from django.test import TestCase

from posts.models import Post


class PostViewTestCase(TestCase):
    def create_post(self, title="new title"):
        return Post.objects.create(title=title)

    def test_detail_view(self):
        obj = self.create_post(title='new title for view test')
        response = self.client.get(obj.get_absolute_url())
        # print(response)
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)

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

    def test_list_view(self):
        obj = self.create_post(title='new title for view test')
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
