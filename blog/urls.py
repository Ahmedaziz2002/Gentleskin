from django.urls import path

from .views import (
    AboutView,
    AffiliateRedirectView,
    CategoryPostListView,
    HomeView,
    PostDetailView,
    PrivacyPolicyView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("category/<slug:slug>/", CategoryPostListView.as_view(), name="category_posts"),
    path("go/<slug:slug>/", AffiliateRedirectView.as_view(), name="affiliate_redirect"),
    path("privacy/", PrivacyPolicyView.as_view(), name="privacy"),
]
