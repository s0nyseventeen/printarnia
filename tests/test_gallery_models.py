from src.gallery.models import Image
from src.gallery.models import Work


def test_image_repr():
    image = Image(id=1, title='image.jpg', description='testing', work_id=1)
    assert repr(image) == '<Image(id=1, title=image.jpg, work_id=1)>'


def test_work_repr():
    work = Work(
        id=1,
        title='New design',
        created='23-12-2023 15:15:22',
        description='Testing'
    )
    assert repr(work) == '<Work(id=1, title=New design, created=23-12-2023 15:15:22)>'
