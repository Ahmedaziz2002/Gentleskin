from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView, View

from .models import Post
from .selectors import get_category_posts, get_home_posts, get_post_detail
from .services import register_affiliate_click


class HomeView(ListView):
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = get_home_posts(self.request.GET.get("page"), self.paginate_by)
        return context


class PostDetailView(DetailView):
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        return get_post_detail(self.kwargs["slug"])


class AboutView(TemplateView):
    template_name = "blog/about.html"


class CategoryPostListView(TemplateView):
    template_name = "blog/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category, posts = get_category_posts(self.kwargs["slug"])
        context["category"] = category
        context["posts"] = posts
        return context


class AffiliateRedirectView(View):
    def get(self, request, slug):
        post = get_post_detail(slug)
        if not post.affiliate_link:
            return redirect(post.get_absolute_url())
        register_affiliate_click(request, post)
        return HttpResponseRedirect(post.affiliate_link)


class PrivacyPolicyView(TemplateView):
    template_name = "privacy.html"
