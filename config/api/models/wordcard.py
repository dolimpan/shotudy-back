from django.db import models


class WordCard(models.Model):
    sentence = models.ForeignKey(
        "api.Sentence",
        on_delete=models.CASCADE,
        related_name="word_cards"
    )

    user = models.ForeignKey(
        "api.User",
        on_delete=models.CASCADE,
        related_name="word_cards"
    )

    word = models.CharField(
        max_length=100
    )

    word_grade =  models.CharField(max_length=2, default="L1")   

    meaning_en = models.CharField(
        max_length=255,
        blank=True
    )

    meaning_kr = models.CharField(
        max_length=255,
        blank=True
    )

    synonym = models.JSONField(
    default=list,
    blank=True
    )

    custom_example = models.CharField(
        max_length=1000,
        blank=True
    )

    is_learned = models.BooleanField(
        null=True, blank=True, default=None
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.word