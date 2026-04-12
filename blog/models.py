from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .querysets import CategoryQuerySet, PostQuerySet


def build_unique_slug(instance, value):
    base_slug = slugify(value)[:50] or "item"
    slug = base_slug
    suffix = 2
    model_class = instance.__class__
    while model_class.objects.exclude(pk=instance.pk).filter(slug=slug).exists():
        slug = f"{base_slug[:44]}-{suffix}"
        suffix += 1
    return slug


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    objects = CategoryQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = build_unique_slug(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_posts", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
    featured_image = models.ImageField(upload_to="posts/", blank=True, null=True)
    excerpt = models.TextField(help_text="Short summary for previews")
    content = models.TextField()
    affiliate_link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["category", "status"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = build_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class AffiliateClick(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="clicks")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    clicked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-clicked_at"]
        indexes = [
            models.Index(fields=["post", "clicked_at"]),
            models.Index(fields=["session_key", "clicked_at"]),
        ]

    def __str__(self):
        return f"Click on {self.post.title}"
