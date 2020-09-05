import os
from django.contrib.staticfiles.storage import staticfiles_storage

from django.urls import reverse

import pyqrcode
from PIL import Image, ImageDraw

from qrforall import settings


def create_qr(obj, category=None, num=None):
    imgname = os.path.join('photos', str(obj.slug), '{}.png'.format(obj.slug))
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'photos', str(obj.slug))):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'photos', str(obj.slug)))
    if num == None or category == None:
        url = pyqrcode.QRCode(
            "{}://{}".format(settings.HTTP_METHOD, settings.SITE_URL) + reverse('menu-detail', args=(obj.slug,)),
            error='H')

    else:
        imgname = os.path.join('photos', str(obj.slug), '{}-{}.png'.format(obj.slug, num))
        url = pyqrcode.QRCode(
            "{}://{}".format(settings.HTTP_METHOD, settings.SITE_URL) + reverse('menu-detail',
                                                                                args=(obj.slug, category, num)),
            error='H')
    scale = 10
    url.png(os.path.join(settings.MEDIA_ROOT, imgname), scale=scale)
    im = Image.open(os.path.join(settings.MEDIA_ROOT, imgname))
    im = im.convert("RGBA")
    if obj.logo and hasattr(obj.logo, 'url'):
        logo = Image.open(obj.logo.path).convert("RGBA")
        logo_size = 41 * 0.3 * scale
        width, height = im.size
        # Calculate xmin, ymin, xmax, ymax to put the logo
        xmin = ymin = int((width / 2) - (logo_size / 2))
        xmax = ymax = int((width / 2) + (logo_size / 2))
        # resize the logo as calculated
        logo = logo.resize((xmax - xmin, ymax - ymin))
        if num == None:
            im.paste(Image.new('RGB', logo.size, (255, 255, 255)), (xmin, ymin, xmax, ymax))
            im.paste(logo, (xmin, ymin, xmax, ymax), logo)
        else:
            im.paste(generate_num(num, logo.size), (xmin, ymin, xmax, ymax))

    # im.paste(generate_num(1), (xmin, ymin, xmax, ymax))
    # im.show()
    im.save(os.path.join(settings.MEDIA_ROOT, imgname))
    # print(settings.MEDIA_URL + imgname)
    return settings.MEDIA_URL + imgname


def generate_num(num, size):
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new('RGB', size, color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(staticfiles_storage.path('fonts/Mukti_Narrow_Bold.ttf'), 64)

    w, h = d.textsize(str(num), font=font)
    d.text(((size[0] - w) / 2, (size[1] - h - h / 2) / 2), str(num), font=font, fill="black")

    return img
