# api/services/image_save_service.py

import os
import uuid

from django.conf import settings
from django.core.files.storage import (
    default_storage
)


def save_image(image):

    ext = os.path.splitext(
        image.name
    )[1]

    filename = (
        f"sentences/"
        f"{uuid.uuid4()}{ext}"
    )

    path = default_storage.save(
        filename,
        image
    )

    return (
        settings.MEDIA_URL
        + path
    )