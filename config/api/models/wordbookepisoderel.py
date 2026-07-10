from django.db import models


class WordBookEpisodeRel(models.Model):
    wordbook = models.ForeignKey(
        "api.WordBook",
        on_delete=models.CASCADE,
        related_name="episode_relations"
    )

    episode = models.ForeignKey(
        "api.Episode",
        on_delete=models.CASCADE,
        related_name="wordbook_relations"
    )

    added_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("wordbook", "episode")

    def __str__(self):
        return f"{self.wordbook.name} - {self.episode}"