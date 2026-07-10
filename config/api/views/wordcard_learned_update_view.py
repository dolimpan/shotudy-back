# api/views/wordcard_learned_update_view.py

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from api.models import WordCard

from api.serializers.wordcard_learned_update_serializer import (
    WordCardLearnedUpdateSerializer
)


class WordCardLearnedUpdateView(
    APIView
):
    permission_classes = [IsAuthenticated]

    def patch(
        self,
        request,
        wordcard_id
    ):
        serializer = (
            WordCardLearnedUpdateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        # -------------------------
        # wordcard validation
        # -------------------------

        wordcard = WordCard.objects.get(
            id=wordcard_id,
            user=request.user
        )

        # -------------------------
        # update
        # -------------------------

        wordcard.is_learned = (
            serializer.validated_data[
                "is_learned"
            ]
        )

        wordcard.save()

        return Response({
            "wordcard_id": wordcard.id,
            "is_learned":
                wordcard.is_learned,
        })