class CreateThumbnail(object):
    """
    Класс для создания миниатюр изображения
    """
    def create_thumbnail(self, from_img, to_img, width, height):
        """
        Создание миниатюры
        """
        if not from_img:
            return

        from PIL import Image, ImageOps
        from io import BytesIO, StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        THUMBNAIL_SIZE = (width, height)

        if from_img.name.endswith(".jpg"):
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
            DJANGO_TYPE = 'image/jpeg'

        elif from_img.name.endswith(".png"):
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
            DJANGO_TYPE = 'image/png'

        images = Image.open(BytesIO(from_img.read()))

        # image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        image = ImageOps.fit(images, THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)


        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField

        suf = SimpleUploadedFile(os.path.split(from_img.name)[-1],
                                 temp_handle.read(), content_type=DJANGO_TYPE)

        # Save SimpleUploadedFile into image field
        to_img.save(
            '%s_thumbnail_160.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )