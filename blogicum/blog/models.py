from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from typing import Type

from .querysets import PostQuerySet

User = get_user_model()

MAX_LENGTH = 256


class BaseModel(models.Model):
    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(
        verbose_name="Добавлено", auto_now_add=True, auto_now=False
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Заголовок"
    )
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; разрешены символы "
            "латиницы, цифры, дефис и подчёркивание."
        ),
        unique=True,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

    def get_absolute_url(self) -> str:
        return reverse(
            "blog:category_posts",
            kwargs={"category_slug": self.slug},
        )


class Location(BaseModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Название места"
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Post(BaseModel):
    author = models.ForeignKey(
        User,
        verbose_name="Автор публикации",
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        Location,
        verbose_name="Местоположение",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        null=True,
    )

    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Заголовок"
    )
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — можно делать "
            "отложенные публикации."
        ),
    )
    image = models.ImageField("Изображение", blank=True, upload_to="img/")

    objects: Type[PostQuerySet] = PostQuerySet.as_manager()

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)
        default_related_name = "posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("blog:post_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Пост",
    )

    text = models.TextField(
        verbose_name="Текст комментария",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)
        default_related_name = "comments"

    def __str__(self):
        return self.text
