# api/views/wordbook_list_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from api.models import (Media,Episode,WordBook,WordBookEpisodeRel,)

from api.serializers.wordbook_list_serializer import (WordBookListSerializer)

from api.serializers.wordbook_auto_create_serializer import (WordBookAutoCreateSerializer)



class WordBookListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wordbooks = WordBook.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = WordBookListSerializer(
            wordbooks,
            many=True
        )

        return Response({
            "wordbooks": serializer.data
        })

    def post(self, request):

        mode = request.data.get("mode")

        # ===================================
        # AUTO
        # ===================================

        if mode == "auto":
            return self.create_auto_wordbook(
                request
            )

        # ===================================
        # MANUAL
        # ===================================

        return self.create_manual_wordbook(
            request
        )


    def create_auto_wordbook(self, request):
        serializer = (
            WordBookAutoCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated = serializer.validated_data

        name = validated["name"]

        lang = validated["lang"]

        media_type = validated["media_type"]

        period = validated["period"]

        from_date = period["from"]

        to_date = period["to"]

        # -------------------------
        # media filtering
        # -------------------------

        medias = Media.objects.filter(
            user=request.user,
            media_type=media_type,
            created_at__date__gte=from_date,
            created_at__date__lte=to_date,
        )

        # -------------------------
        # episode collect
        # -------------------------

        episodes = Episode.objects.filter(
            media_id__in=medias
        )

        # -------------------------
        # wordbook create
        # -------------------------

        wordbook = WordBook.objects.create(
            user=request.user,
            name=name,
            lang=lang,
            is_auto=True
        )

        # -------------------------
        # rel bulk create
        # -------------------------

        rels = []

        for episode in episodes:
            rels.append(
                WordBookEpisodeRel(
                    wordbook=wordbook,
                    episode=episode
                )
            )

        WordBookEpisodeRel.objects.bulk_create(
            rels
        )

        return Response({
            "word_book_id": wordbook.id,
            "is_auto": True
        })

    def create_manual_wordbook(
        self,
        request
    ):
        serializer = (
            WordBookManualCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated = serializer.validated_data

        wordbook = WordBook.objects.create(
            user=request.user,
            name=validated["name"],
            lang=validated["lang"],
            is_auto=False
        )

        return Response({
            "word_book_id": wordbook.id,
            "is_auto": False
        })
    