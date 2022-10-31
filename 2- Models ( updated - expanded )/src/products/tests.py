from django.test import TestCase
from django.utils.text import slugify

from .models import Product


class ProductTestCase(TestCase):
    # fixtures = ['products/fixtures/products/products']

    def our_date(self):
        date = {
            'title': 'Our Title',
            'price': 12.65
        }
        self.draft_a = Product.objects.create(**date)
        self.draft_b = Product.objects.create(**date)
        self.draft_c = Product.objects.create(**date)
        self.count = 3

    def our_data_published_state(self):
        date = {
            'title': 'Published State Title',
            'price': 15.66,
            'state': Product.STATE_CHOICES.PUBLIC
        }
        self.pub_a = Product.objects.create(**date)
        self.pub_b = Product.objects.create(**date)
        self.pub_c = Product.objects.create(**date)
        self.pub_count = 3

    def our_slug_test(self):
        self.title = "Hello it's our test for Slug and it's number 48789 for test numbers"
        date = {
            'title': self.title,
            'price': 45.56
        }
        self.slug_title = self.title
        self.slug_slug = slugify(self.title)
        self.slug_a = Product.objects.create(**date)
        self.slug_b = Product.objects.create(**date)
        self.slug_c = Product.objects.create(**date)
        self.slug_count = 3

    def setUp(self):
        self.our_date()
        self.our_data_published_state()
        self.our_slug_test()

    def test_draft_items(self):
        qs = Product.objects.all()
        self.assertTrue(qs.exists())

    def test_draft_count(self):
        qs = Product.objects.filter(state=Product.STATE_CHOICES.PRIVATE)
        self.assertEqual(qs.count(), self.count + self.slug_count)

    # Published State
    def test_published_state(self):
        qs = Product.objects.filter(state=Product.STATE_CHOICES.PUBLIC)
        self.assertEqual(qs.count(), self.pub_count)

    # property
    def test_public_property(self):
        self.assertTrue(self.pub_a.is_public)
        self.assertTrue(self.pub_b.is_public)
        self.assertTrue(self.pub_c.is_public)

    # Manager and Custome QuerySet
    def test_manager_and_custome_queryset(self):
        manager_qs = Product.objects.published()
        custome_qs = Product.objects.all().published_products()
        self.assertEqual(manager_qs.count(),
                         custome_qs.count(), self.pub_count)

        manager_qs_ids = list(manager_qs.values_list('id', flat=True))
        custome_qs_ids = list(custome_qs.values_list('id', flat=True))
        self.assertEqual(manager_qs_ids, custome_qs_ids)
        self.assertEquals(len(manager_qs_ids), len(custome_qs_ids))

    # test slug
    def test_slug_title_signal(self):
        self.assertEqual(self.slug_slug, self.slug_a.slug)

    # Test slug unique
    def test_slug_unique(self):
        self.assertNotEqual(self.slug_slug, self.slug_b.slug)
        self.assertNotEqual(self.slug_slug, self.slug_c.slug)
        self.assertNotEqual(self.slug_b.slug, self.slug_c.slug)

    def test_slug_count(self):
        qs = Product.objects.filter(slug__icontains=self.slug_slug)
        self.assertEqual(qs.count(), self.slug_count)
