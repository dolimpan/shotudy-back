from django.db import models


class Sentence(models.Model):
    episode = models.ForeignKey(
        "api.Episode",
        on_delete=models.CASCADE,
        related_name="sentences"
    )

    user = models.ForeignKey(
        "api.User",
        on_delete=models.CASCADE,
        related_name="sentences"
    )

    speaker = models.CharField(
        max_length=100,
        blank=True
    )

    script = models.CharField(
        max_length=1000
    )

    img_url = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.script[:50]