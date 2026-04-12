from django.test import TestCase
from django.urls import reverse

from .models import AffiliateClick, Category, Post


class BlogViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Cleansers")
        self.published_post = Post.objects.create(
            title="Barrier First Routine",
            category=self.category,
            excerpt="A calm routine for reactive skin.",
            content="Step one\nStep two",
            affiliate_link="https://example.com/product",
            status=Post.Status.PUBLISHED,
        )
        self.draft_post = Post.objects.create(
            title="Draft Routine",
            category=self.category,
            excerpt="Hidden draft.",
            content="Draft content",
            status=Post.Status.DRAFT,
        )

    def test_category_has_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(), f"/category/{self.category.slug}/")

    def test_home_displays_only_published_posts(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, self.published_post.title)
        self.assertNotContains(response, self.draft_post.title)

    def test_affiliate_redirect_creates_one_click_per_session_window(self):
        url = reverse("affiliate_redirect", args=[self.published_post.slug])
        first_response = self.client.get(url)
        second_response = self.client.get(url)
        self.assertEqual(first_response.status_code, 302)
        self.assertEqual(second_response.status_code, 302)
        self.assertEqual(AffiliateClick.objects.filter(post=self.published_post).count(), 1)
