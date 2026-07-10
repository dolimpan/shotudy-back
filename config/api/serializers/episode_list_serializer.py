# api/serializers/episode_list_serializer.py

from rest_framework import serializers

from api.models import Episode


class EpisodeListSerializer(
    serializers.ModelSerializer
):
    episode_id = serializers.IntegerField(
        source="id"
    )

    episode_title = serializers.CharField(
        source="title"
    )

    media_id = serializers.SerializerMethodField()

    media_title = serializers.SerializerMethodField()

    class Meta:
        model = Episode

        fields = [
            "episode_id",
            "episode_title",

            "media_id",
            "media_title",

            "sequence_number",
        ]

    def get_media_id(self, obj):
        return obj.media_id.id

    def get_media_title(self, obj):
        return obj.media_id.title