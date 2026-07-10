# api/serializers/wordbook_episode_update_serializer.py

from rest_framework import serializers


class EpisodeItemSerializer(
    serializers.Serializer
):
    episode_id = serializers.IntegerField()


class WordBookEpisodeUpdateSerializer(
    serializers.Serializer
):
    episodes = EpisodeItemSerializer(
        many=True
    )