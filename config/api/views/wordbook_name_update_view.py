# api/views/wordbook_name_update_view.py

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from api.models import WordBook

from api.serializers.wordbook_name_update_serializer import (
    WordBookNameUpdateSerializer
)


class WordBookNameUpdateView(
    APIView
):
    permission_classes = [IsAuthenticated]

    def patch(
        self,
        request,
        word_book_id
    ):
        serializer = (
            WordBookNameUpdateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        # -------------------------
        # validation
        # -------------------------

        wordbook = WordBook.objects.get(
            id=word_book_id,
            user=request.user
        )

        # -------------------------
        # update
        # -------------------------

        wordbook.name = (
            serializer.validated_data[
                "name"
            ]
        )

        wordbook.save()

        return Response({
            "word_book_id":
                wordbook.id,

            "name":
                wordbook.name,
        })