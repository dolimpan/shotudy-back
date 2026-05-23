# api/views/wordbook_episode_update_view.py

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework import status

from api.models import (
    WordBook,
    Episode,
    WordBookEpisodeRel,
)

from api.serializers.wordbook_episode_update_serializer import (
    WordBookEpisodeUpdateSerializer
)


class WordBookEpisodeUpdateView(
    APIView
):
    permission_classes = [IsAuthenticated]

    def put(
        self,
        request,
        word_book_id
    ):
        serializer = (
            WordBookEpisodeUpdateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        # -------------------------
        # wordbook validation
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
                    "Auto wordbook cannot be modified."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -------------------------
        # existing rel delete
        # -------------------------

        WordBookEpisodeRel.objects.filter(
            wordbook=wordbook
        ).delete()

        # -------------------------
        # recreate rels
        # -------------------------

        created_episode_ids = []

        rels = []

        for item in (
            serializer.validated_data[
                "episodes"
            ]
        ):
            episode = Episode.objects.get(
                id=item["episode_id"]
            )

            rels.append(
                WordBookEpisodeRel(
                    wordbook=wordbook,
                    episode=episode
                )
            )

            created_episode_ids.append(
                episode.id
            )

        WordBookEpisodeRel.objects.bulk_create(
            rels
        )

        return Response({
            "episode_ids":
                created_episode_ids
        })