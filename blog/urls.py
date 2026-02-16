from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),
    path("go/<slug:slug>/", views.affiliate_redirect, name="affiliate_redirect"),
    path("privacy/", views.privacy_policy, name="privacy"),
]
