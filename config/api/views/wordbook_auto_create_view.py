# api/views/wordbook_auto_create_view.py

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from api.models import (
    Media,
    Episode,
    WordBook,
    WordBookEpisodeRel,
)

from api.serializers.wordbook_auto_create_serializer import (
    WordBookAutoCreateSerializer
)


class WordBookAutoCreateView(
    APIView
):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = (
            WordBookAutoCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated = serializer.validated_data

        name = validated["name"]

        lang = validated["lang"]

        media_type = validated["media_type"]

        period = validated["period"]

        from_date = period["from"]

        to_date = period["to"]

        # -------------------------
        # media filtering
        # -------------------------

        medias = Media.objects.filter(
            user=request.user,
            media_type=media_type,
            created_at__date__gte=from_date,
            created_at__date__lte=to_date,
        )

        # -------------------------
        # episode collect
        # -------------------------

        episodes = Episode.objects.filter(
            media_id__in=medias
        )

        # -------------------------
        # wordbook create
        # -------------------------

        wordbook = WordBook.objects.create(
            user=request.user,
            name=name,
            lang=lang,
            is_auto=True
        )

        # -------------------------
        # rel bulk create
        # -------------------------

        rels = []

        for episode in episodes:
            rels.append(
                WordBookEpisodeRel(
                    wordbook=wordbook,
                    episode=episode
                )
            )

        WordBookEpisodeRel.objects.bulk_create(
            rels
        )

        return Response({
            "word_book_id": wordbook.id,
            "is_auto": True
        })