# api/views/wordbook_delete_view.py

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework import status

from api.models import WordBook


class WordBookDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(
        self,
        request,
        word_book_id
    ):
        # -------------------------
        # validation
        # -------------------------

        wordbook = WordBook.objects.get(
            id=word_book_id,
            user=request.user
        )

        # -------------------------
        # auto forbidden
        # -------------------------

        if wordbook.is_auto:
            return Response(
                {
                    "detail":
                    "Auto wordbook cannot be deleted."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        deleted_id = wordbook.id

        # -------------------------
        # delete
        # -------------------------

        wordbook.delete()

        return Response({
            "word_book_id":
                deleted_id
        })