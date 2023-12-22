import io

from flask import request

from src.lib.request_helpers import get_img_info


def test_get_img_info(create_work, app):
    with app.test_request_context(
        '/1/update/images/detail/1',
        method='POST',
        data={
            'image': (io.BytesIO(b'randomstr'), 'image.jpg'),
            'image_description': 'Description'
        },
        content_type='multipart/form-data'
    ):
        img, description = get_img_info(request)
    assert img.filename == 'image.jpg'
    assert description == 'Description'
