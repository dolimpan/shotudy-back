from django.db import models


class WordBook(models.Model):
    user = models.ForeignKey(
        "api.User",
        on_delete=models.CASCADE,
        related_name="wordbooks"
    )

    media = models.ForeignKey(
        "api.Media",
        on_delete=models.SET_NULL,
        related_name="wordbooks",
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    lang = models.CharField(
        max_length=30
    )

    is_auto = models.BooleanField(
        default=False
    )

    last_viewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name