from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated
)

from api.models.episode import Episode

# -----------------------------
# services
# -----------------------------

from api.services.ocr_service import (
    extract_text
)

from api.services.llm_service import (
    analyze_text
)

from api.services.translate_service import (
    translate_sentences
)

from api.services.save_script_service import (
    save_sentences
)

from api.services.extract_words_service import (
    extract_words
)

from api.services.enrich_words_service import (
    enrich_words
)

from api.services.save_wordcards_service import (
    save_wordcards
)

from api.services.image_save_service import (
    save_image
)

class AnalyzeSaveView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request,
        episode_id
    ):

        # ---------------------------------
        # image validation
        # ---------------------------------

        image = request.FILES.get(
            "image"
        )

        if not image:

            return Response(
                {
                    "error":
                    "이미지 없음"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ---------------------------------
        # episode validation
        # ---------------------------------

        try:

            episode = Episode.objects.get(
                id=episode_id
            )

        except Episode.DoesNotExist:

            return Response(
                {
                    "error":
                    "episode 없음"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        image_url = save_image(image)

        # ---------------------------------
        # 1. OCR
        # ---------------------------------

        image.seek(0)
        
        raw_text = extract_text(
            image
        )

        # ---------------------------------
        # 2. sentence restore
        # ---------------------------------

        restored_sentences = analyze_text(
            raw_text
        )

        # ---------------------------------
        # 3. translate
        # ---------------------------------

        translated_sentences = (
            translate_sentences(
                restored_sentences
            )
        )

        # ---------------------------------
        # 4. sentence save
        # ---------------------------------

        saved_sentence_rows = (
            save_sentences(
                translated_sentences,
                request.user,
                 episode,
                image_url
            )
        )

        # ---------------------------------
        # 5. extract words
        # ---------------------------------

        extracted_words = (
            extract_words(
                saved_sentence_rows
            )
        )

        # ---------------------------------
        # 6. enrich words
        # ---------------------------------

        enriched_words = (
            enrich_words(
                extracted_words
            )
        )

        # ---------------------------------
        # 7. save wordcards
        # ---------------------------------

        saved_wordcards = (
            save_wordcards(
                enriched_words,
                request.user
            )
        )

        # ---------------------------------
        # response
        # ---------------------------------

        return Response({

            "message": "success",

            "saved_sentence_count":
                len(saved_sentence_rows),

            "saved_wordcard_count":
                len(saved_wordcards),

            "sentences":
                translated_sentences,

            "words":
                enriched_words
        })