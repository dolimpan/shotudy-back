# api/serializers/wordbook_auto_create_serializer.py

from rest_framework import serializers


class PeriodSerializer(serializers.Serializer):
    from_date = serializers.DateField(
        source="from"
    )

    to_date = serializers.DateField(
        source="to"
    )


class WordBookAutoCreateSerializer(
    serializers.Serializer
):
    name = serializers.CharField()

    lang = serializers.CharField()

    mode = serializers.CharField()

    media_type = serializers.CharField()

    period = PeriodSerializer()