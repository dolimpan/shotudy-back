# api/views/wordbook_wordcard_list_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.models import (
    WordBook,
    WordBookEpisodeRel,
    WordCard,
)

from api.serializers.wordcard_list_serializer import (
    WordCardListSerializer
)


class WordBookWordCardListView(
    APIView
):
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
        word_book_id
    ):
        # 단어장 검증
        wordbook = WordBook.objects.get(
            id=word_book_id,
            user=request.user
        )

        # 연결된 episode들
        rels = WordBookEpisodeRel.objects.filter(
            wordbook=wordbook
        )

        episode_ids = [
            rel.episode.id
            for rel in rels
        ]

        # 해당 episode의 sentence 기반 wordcard
        wordcards = WordCard.objects.filter(
            sentence__episode__id__in=episode_ids,
            user=request.user
        ).select_related(
            "sentence",
            "sentence__episode",
            "sentence__episode__media_id"
        )

        serializer = WordCardListSerializer(
            wordcards,
            many=True
        )

        return Response({
            "wordcards": serializer.data
        })