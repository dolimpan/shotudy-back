# api/serializers/wordcard_list_serializer.py

from rest_framework import serializers

from api.models import WordCard


class WordCardListSerializer(
    serializers.ModelSerializer
):
    wordcard_id = serializers.IntegerField(
        source="id"
    )

    media_id = serializers.SerializerMethodField()

    episode_id = serializers.SerializerMethodField()

    sentence_id = serializers.SerializerMethodField()

    speaker = serializers.CharField(
        source="sentence.speaker"
    )

    script = serializers.CharField(
        source="sentence.script"
    )

    class Meta:
        model = WordCard

        fields = [
            "wordcard_id",

            "media_id",
            "episode_id",
            "sentence_id",

            "word",
            "word_grade",
            "meaning_en",
            "meaning_kr",
            "synonym",
            "custom_example",
            "is_learned",

            "speaker",
            "script",
        ]

    def get_media_id(self, obj):
        return (
            obj.sentence
            .episode
            .media_id
            .id
        )

    def get_episode_id(self, obj):
        return obj.sentence.episode.id

    def get_sentence_id(self, obj):
        return obj.sentence.id