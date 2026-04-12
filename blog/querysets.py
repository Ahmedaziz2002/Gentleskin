from django.db import models
from django.db.models import Count


class CategoryQuerySet(models.QuerySet):
    def ordered(self):
        return self.order_by("name")

    def for_navigation(self):
        return self.ordered().only("name", "slug")


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="published")

    def with_related(self):
        return self.select_related("category")

    def with_click_totals(self):
        return self.annotate(click_count=Count("clicks"))
