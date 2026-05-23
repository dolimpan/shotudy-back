# api/views/episode_list_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)

from api.models import Episode

from api.serializers.episode_list_serializer import (
    EpisodeListSerializer
)


class EpisodeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        episodes = Episode.objects.filter(
            media_id__user=request.user
        ).select_related(
            "media_id"
        ).order_by(
            "media_id",
            "sequence_number"
        )

        serializer = EpisodeListSerializer(
            episodes,
            many=True
        )

        return Response({
            "episodes": serializer.data
        })