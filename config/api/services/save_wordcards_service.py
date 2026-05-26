# api/services/save_wordcards_service.py

from api.models.wordcard import (
    WordCard
)

from api.models.sentence import (
    Sentence
)


def save_wordcards(
    enriched_words,
    user
):

    created_cards = []

    for item in enriched_words:

        try:

            sentence = (
                Sentence.objects.get(
                    id=item["sentence_id"]
                )
            )

        except Sentence.DoesNotExist:

            continue

        row = WordCard.objects.create(

            sentence=sentence,

            user=user,

            word=item["word"],

            word_grade=item.get(
                "word_grade",
                "L1"
            ),

            meaning_kr=item.get(
                "meaning_kr",
                ""
            ),

            meaning_en=item.get(
                "meaning_en",
                ""
            ),

            synonym=item.get(
                "synonym",
                []
            ),

            custom_example=item.get(
                "custom_example",
                ""
            ),

            is_learned=False
        )

        created_cards.append(
            row
        )

    return created_cards