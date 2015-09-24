import math

from wagtail.wagtailcore import hooks
from wagtail.wagtailimages.image_operations import FillOperation


class CustomFillOperation(FillOperation):
    vary_fields = (
        'focal_point_width', 'focal_point_height',
        'focal_point_x', 'focal_point_y',
        'brightness',
    )

    def run(self, willow, image):
        super().run(willow, image)

        if image.brightness != 0:
            adjust = math.floor(255 * (image.brightness / 100))

            im1 = willow.backend.image

            data = [
                (
                    max(0, r + adjust),
                    max(0, g + adjust),
                    max(0, b + adjust),
                )
                for r, g, b in im1.getdata()
            ]

            im1.putdata(data)

            willow.backend.image = im1


@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('xfill', CustomFillOperation),
    ]
