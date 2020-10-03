import os

from image_optimizer.utils import image_optimizer

from qrback.models import Company, Entry, FoodCategory

from qrforall import settings

from PIL import Image

from resizeimage import resizeimage

BACKGROUND_TRANSPARENT = (255, 255, 255, 0)


def post_image(image):
    output_size = (480, 360)
    image = resizeimage.resize_cover(image, output_size, validate=False)

    output_image = Image.new('RGBA', output_size, BACKGROUND_TRANSPARENT)
    output_image_center = (int((output_size[0] - image.size[0]) / 2),
                           int((output_size[1] - image.size[1]) / 2))

    output_image.paste(image, output_image_center)
    return output_image


def optimize_images():
    # all images in Entry model
    images = list(Entry.objects.values_list('image', flat=True))
    # all images in FoodCategory model
    images.extend(list(FoodCategory.objects.values_list('image', flat=True)))
    # all images in company logos
    images.extend(list(Company.objects.values_list('logo', flat=True)))
    # all images in company banner
    images.extend(list(Company.objects.values_list('menu_background', flat=True)))

    # Optimize images %70 reduction
    for image in images:
        if image != "" and image is not None:
            if image.split('.')[-1] != "JPEG":
                print('{} is not null or blank starting optimization process'.format(image))
                image_path = os.path.join(settings.MEDIA_ROOT, image)
                im = Image.open(image_path)
                im = post_image(im).convert('RGB')
                # print('{} was successfully opened'.format(image))
                im.save(os.path.join(settings.MEDIA_ROOT, image), format="JPEG", quality=70)
                # print('{} was successfully saved wit %70 quality'.format(image))
            else:
                print('{} was JPEG it wont be reduced'.format(image))
