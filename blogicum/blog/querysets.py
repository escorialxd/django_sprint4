from django.db import models
from django.utils import timezone
from django.db.models import Count


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )

    def with_related(self):
        return self.select_related(
            "category",
            "author",
            "location"
        )

    def order_by_date(self):
        return self.order_by("-pub_date")

    def with_comment_count(self):
        return self.annotate(comment_count=Count("comments"))
