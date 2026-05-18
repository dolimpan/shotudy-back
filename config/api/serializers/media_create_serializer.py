# api/serializers/media_create_serializer.py

from rest_framework import serializers


class MediaEpisodeCreateSerializer(serializers.Serializer):
    media_type = serializers.CharField(
        max_length=20
    )

    media_title = serializers.CharField(
        max_length=255
    )

    episode_title = serializers.CharField(
        max_length=255
    )

    sequence_number = serializers.IntegerField(
        min_value=1
    )