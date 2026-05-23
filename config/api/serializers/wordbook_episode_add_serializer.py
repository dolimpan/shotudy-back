# api/serializers/wordbook_episode_add_serializer.py

from rest_framework import serializers


class WordBookEpisodeAddSerializer(
    serializers.Serializer
):
    episode_id = serializers.IntegerField()