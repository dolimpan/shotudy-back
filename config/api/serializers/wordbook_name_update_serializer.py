# api/serializers/wordbook_name_update_serializer.py

from rest_framework import serializers


class WordBookNameUpdateSerializer(
    serializers.Serializer
):
    name = serializers.CharField(
        max_length=100
    )