# api/views/wordbook_delete_view.py

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework import status

from api.models import WordBook


from api.serializers.wordbook_name_update_serializer import (
    WordBookNameUpdateSerializer
)


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