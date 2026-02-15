from django.shortcuts import render, get_object_or_404
from .models import Post, Category


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
