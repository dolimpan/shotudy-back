from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.media import Media
from api.models.episode import Episode
from api.models.wordbook import WordBook
from api.models.wordbook_episode_rel import (
    WordBookEpisodeRel
)

from api.serializers.media_create_serializer import (
    MediaEpisodeCreateSerializer,
)


class MediaEpisodeCreateView(APIView): permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = MediaEpisodeCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = (
            serializer.validated_data
        )

        media_title = (
            validated_data["media_title"]
        )

        media_type = (
            validated_data["media_type"]
        )

        episode_title = (
            validated_data["episode_title"]
        )

        sequence_number = (
            validated_data["sequence_number"]
        )

        # ---------------------------------
        # media get or create
        # ---------------------------------

        media = Media.objects.filter(
            user=request.user,
            title=media_title
        ).first()

        if media is None:

            media = Media.objects.create(
                user=request.user,
                media_type=media_type,
                title=media_title,
            )

        # ---------------------------------
        # episode get or create
        # ---------------------------------

        episode = Episode.objects.filter(
            media_id=media,
            sequence_number=sequence_number
        ).first()

        if episode is None:

            episode = Episode.objects.create(
                media_id=media,
                sequence_number=sequence_number,
                title=episode_title,
            )

        # ---------------------------------
        # auto wordbook get or create
        # ---------------------------------

        wordbook = WordBook.objects.filter(
            user=request.user,
            name=media.title,
            is_auto=True
        ).first()

        if wordbook is None:

            wordbook = WordBook.objects.create(
                user=request.user,
                name=media.title,
                lang="en",
                is_auto=True
            )

        # ---------------------------------
        # episode relation get or create
        # ---------------------------------

        WordBookEpisodeRel.objects.get_or_create(
            wordbook=wordbook,
            episode=episode
        )

        return Response(
            {
                "media_id": media.id,
                "episode_id": episode.id,
                "word_book_id": wordbook.id,
            },
            status=status.HTTP_201_CREATED
        )