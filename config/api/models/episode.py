from django.db import models


class Episode(models.Model):
    media_id = models.ForeignKey(
        "api.Media",
        on_delete=models.CASCADE,
        related_name="episodes"
    )

    sequence_number = models.IntegerField()

    title = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.media_id.title} - EP.{self.sequence_number}"