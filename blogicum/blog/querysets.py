from django.db import models
from django.utils import timezone
from django.db.models import Count


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def with_related(self):
        return self.select_related("category",
                                   "author",
                                   "location"
                                   )

    def filter_by_pub_date(self):
        return self.filter(pub_date__lte=timezone.now(),
                           category__is_published=True)

    def order_by_date(self):
        return self.order_by("-pub_date")

    def with_comment_count(self):
        return self.annotate(comment_count=Count("comments"))

    def for_author(self, username):
        return self.filter(author__username=username)

    def for_category(self, category_slug):
        return self.filter(category__slug=category_slug)
