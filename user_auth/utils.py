import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def imageResize(file):
    img = Image.open(file)

    # Checking if the image is RGB
    if img.mode != "RGB":
        img = img.convert('RGB')

    output = io.BytesIO()

    # Resizing and saving the Image
    height = img.height 
    width = img.width 
    img = img.resize((int(width), int(height)))
    img.save(output, format='JPEG', quality=60)
    output.seek(0)

    file = InMemoryUploadedFile(output, 'ImageFile', "%s.jpg" % file.name.split('.')[0], 'image/jpeg', len(output.getvalue()), None)

    return file
