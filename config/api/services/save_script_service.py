from api.models.sentence import Sentence

def save_sentences(
    translated,
    user,
    episode,
    image_url
):
    created_rows = []

    for item in translated:

        row = Sentence.objects.create(
            episode=episode,

            user=user,

            speaker=item["speaker"],

            script=item["script"],

            img_url=image_url
        )

        created_rows.append(row)

    return created_rows