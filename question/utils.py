'''
def clean_profile_picture(self):
        profile_picture = self.files.get('profile_picture')
        if profile_picture:
            import base64
            from io import BytesIO
            from PIL import Image

            image = Image.open(profile_picture)
            buffered = BytesIO()
            image.save(buffered, format=image.format)
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return img_base64
        return None

'''

import os
import base64
from PIL import Image
from io import BytesIO

def convert_and_remove_images(instance, image_fields):
    for img_field in image_fields:
        img_instance = getattr(instance, img_field)

        if img_instance:
            img_base64_field = f'{img_field}_base64'
            setattr(instance, img_base64_field, image_to_base64(img_instance))
            if os.path.isfile(img_instance.path):
                os.remove(img_instance.path)
            setattr(instance, img_field, None) 

def image_to_base64(image_file):
    image = Image.open(image_file)
    buffered = BytesIO()
    image_format = image.format
    image.save(buffered, format=image_format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str
