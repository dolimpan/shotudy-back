# api/serializers/wordcard_learned_update_serializer.py

from rest_framework import serializers


class WordCardLearnedUpdateSerializer(
    serializers.Serializer
):
    is_learned = serializers.BooleanField()