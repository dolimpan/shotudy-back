# api/serializers/wordbook_manual_create_serializer.py

from rest_framework import serializers


class WordBookManualCreateSerializer(
    serializers.Serializer
):
    name = serializers.CharField()

    lang = serializers.CharField()