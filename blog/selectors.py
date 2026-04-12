from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .models import Category, Post


def get_navigation_categories():
    return Category.objects.for_navigation()


def get_home_posts(page_number, per_page=6):
    queryset = (
        Post.objects.published()
        .with_related()
        .only(
            "title",
            "slug",
            "excerpt",
            "featured_image",
            "created_at",
            "category__name",
            "category__slug",
        )
    )
    return Paginator(queryset, per_page).get_page(page_number)


def get_post_detail(slug):
    return get_object_or_404(Post.objects.published().with_related(), slug=slug)


def get_category_posts(slug):
    category = get_object_or_404(Category.objects.only("name", "slug"), slug=slug)
    posts = (
        Post.objects.published()
        .with_related()
        .filter(category=category)
        .only(
            "title",
            "slug",
            "excerpt",
            "featured_image",
            "created_at",
            "category__name",
            "category__slug",
        )
    )
    return category, posts
