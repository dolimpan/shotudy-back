# api/serializers/wordbook_list_serializer.py

from rest_framework import serializers

from api.models import (
    WordBook,
    WordBookEpisodeRel,
)


class EpisodeInWordBookSerializer(
    serializers.Serializer
):
    episode_id = serializers.IntegerField()
    episode_title = serializers.CharField()
    sequence_number = serializers.IntegerField()


class WordBookListSerializer(
    serializers.ModelSerializer
):
    word_book_id = serializers.IntegerField(
        source="id"
    )

    episodes = serializers.SerializerMethodField()

    class Meta:
        model = WordBook

        fields = [
            "word_book_id",
            "name",
            "lang",
            "is_auto",
            "last_viewed_at",
            "created_at",
            "updated_at",
            "episodes",
        ]

    def get_episodes(self, obj):
        rels = WordBookEpisodeRel.objects.filter(
            wordbook=obj
        )

        episodes = []

        for rel in rels:
            episode = rel.episode

            episodes.append({
                "episode_id": episode.id,
                "episode_title": episode.title,
                "sequence_number": (
                    episode.sequence_number
                )
            })

        return episodes