from django.test import TestCase
from django.utils.text import slugify

from .models import Main


class MainTestCase(TestCase):
    def our_data(self):
        data = {
            'title': 'Title For Test',
            'state': Main.STATE_CHOICES.PUBLIC
        }
        self.draft_a = Main.objects.create(**data)
        self.draft_b = Main.objects.create(**data)
        self.count = 8
        return data

    def public_state_data(self):
        data = {
            'title': 'Title For Test',
            'state': Main.STATE_CHOICES.PRIVATE
        }
        self.new_data = self.our_data()
        self.state_a = Main.objects.create(**data)
        self.state_b = Main.objects.create(**data)
        self.state_c = Main.objects.create(**self.new_data)
        self.state_count = 2

    def our_slug_test(self):
        self.title = "Hello it's our test for Slug and it's number 48789 for test numbers"
        date = {
            'title': self.title,
        }
        self.slug_slug = slugify(self.title)
        self.slug_a = Main.objects.create(**date)
        self.slug_b = Main.objects.create(**date)
        self.slug_c = Main.objects.create(**date)
        self.slug_count = 3

    def setUp(self):
        self.our_data()
        self.public_state_data()
        self.our_slug_test()

    # Unit One -> Correct setup data
    def test_main_models(self):
        qs = Main.objects.all()
        self.assertTrue(qs.exists())

    def test_count_obj(self):
        qs = Main.objects.filter(active=True)
        self.assertEqual(qs.count(), self.count)

    # Unit Tow -> Public Data
    def test_public_state(self):
        qs = Main.objects.filter(state=Main.STATE_CHOICES.PRIVATE)
        self.assertEqual(qs.count(), self.state_count)

    def test_property(self):
        self.assertTrue(self.state_a.is_private)
        self.assertTrue(self.state_b.is_private)
        self.assertTrue(self.state_c.active)

    # Unit Three -> Public Data
    def test_custom_Manager_and_queryset(self):
        manager_qs = Main.objects.is_private_manager()
        queryset_qs = Main.objects.all().is_public()
        self.assertEqual(manager_qs.count(),
                         queryset_qs.count(), self.count + 1)

        manager_qs_ids = list(manager_qs.values_list('id', flat=True))
        custome_qs_ids = list(queryset_qs.values_list('id', flat=True))
        self.assertEqual(manager_qs_ids, custome_qs_ids)
        self.assertEquals(len(manager_qs_ids), len(custome_qs_ids))

    # Unit Three -> Slug
    def test_slug(self):
        self.assertEqual(self.slug_slug, self.slug_a.slug)

    def test_unique_slug(self):
        self.assertNotEqual(self.slug_a.slug, self.slug_b.slug)
        self.assertNotEqual(self.slug_a.slug, self.slug_c.slug)
        self.assertNotEqual(self.slug_c.slug, self.slug_b.slug)

    def test_count_slug(self):
        qs = Main.objects.filter(slug__icontains=self.slug_slug)
        self.assertEqual(qs.count(), self.slug_count)
