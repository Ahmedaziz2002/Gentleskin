from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import timedelta
from .models import Post, Category, AffiliateClick


from django.core.paginator import Paginator

def home(request):
    post_list = Post.objects.filter(status="published")
    paginator = Paginator(post_list, 6)

    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    return render(request, "blog/home.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    return render(request, "blog/post_detail.html", {"post": post})


def about(request):
    return render(request, "blog/about.html")

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status="published")
    return render(request, "blog/category.html", {
        "category": category,
        "posts": posts
    })

def affiliate_redirect(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")

    # Ensure session exists
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    ip_address = request.META.get("REMOTE_ADDR")
    user_agent = request.META.get("HTTP_USER_AGENT")

    # Check if this user already clicked within 24 hours
    recent_click = AffiliateClick.objects.filter(
        post=post,
        ip_address=ip_address,
        clicked_at__gte=timezone.now() - timedelta(hours=24)
    ).exists()

    if not recent_click:
        AffiliateClick.objects.create(
            post=post,
            ip_address=ip_address,
            user_agent=user_agent,
            session_key=session_key
        )

    return redirect(post.affiliate_link)

def privacy_policy(request):
    return render(request, "privacy.html")
