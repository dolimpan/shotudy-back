# api/views/media_create_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.media import Media
from api.models.episode import Episode
from api.models.user import User

from api.serializers.media_create_serializer import (
    MediaEpisodeCreateSerializer,
)


class MediaEpisodeCreateView(APIView):
    def post(self, request):
        serializer = MediaEpisodeCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        media = Media.objects.create(
            user=request.user,
            media_type=validated_data["media_type"],
            title=validated_data["media_title"],
        )

        episode = Episode.objects.create(
            media_id=media,
            sequence_number=validated_data["sequence_number"],
            title=validated_data["episode_title"],
        )

        return Response(
            {
                "media_id": media.id,
                "episode_id": episode.id,
            },
            status=status.HTTP_201_CREATED
        )