# api/views/wordbook_episode_delete_view.py

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework import status

from api.models import (
    WordBook,
    WordBookEpisodeRel,
)


class WordBookEpisodeDeleteView(
    APIView
):
    permission_classes = [IsAuthenticated]

    def delete(
        self,
        request,
        word_book_id,
        episode_id
    ):
        # -------------------------
        # wordbook validation
        # -------------------------

        wordbook = WordBook.objects.get(
            id=word_book_id,
            user=request.user
        )

        # -------------------------
        # auto wordbook forbidden
        # -------------------------

        if wordbook.is_auto:
            return Response(
                {
                    "detail":
                    "Auto wordbook cannot be modified."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -------------------------
        # relation find
        # -------------------------

        rel = (
            WordBookEpisodeRel.objects.get(
                wordbook=wordbook,
                episode_id=episode_id
            )
        )

        # -------------------------
        # delete
        # -------------------------

        rel.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )