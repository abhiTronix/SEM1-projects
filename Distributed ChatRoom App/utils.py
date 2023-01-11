import io
import zlib
from PIL import Image

MAX_WIDTH = 500
MAX_HEIGHT = 500


def resize_image_with_aspect_ratio(image, size=(1000, 1000)):
    """
    Resize a PIL.Image while maintaining aspect ratio.
    """
    image.thumbnail(size, Image.ANTIALIAS)
    return image


def convert_bytes_to_image(byte_data, width, height, rgb):
    """
    Transforms byte data of an image to PIL.Image object.
    """
    if not rgb:
        img = Image.frombytes(
            mode="L", size=(width, height), data=zlib.decompress(byte_data)
        )
    else:
        img = Image.frombytes(
            mode="RGB", size=(width, height), data=zlib.decompress(byte_data)
        )
    return img


def convert_image_n_save(image, outfile):
    size = (MAX_WIDTH, MAX_HEIGHT)
    if image.width > MAX_WIDTH or image.height > MAX_HEIGHT:
        print("Image is too large. Resizing...")
        image = resize_image_with_aspect_ratio(image, size)
    save_image(image=image, outfile=outfile)


def convert_image_to_Image(image, rgb):
    """
    Converts a PIL.Image object to ImageData.
    """
    img_data = []
    size = (MAX_WIDTH, MAX_HEIGHT)
    if image.width > MAX_WIDTH or image.height > MAX_HEIGHT:
        print("Image is too large. Resizing...")
        image = resize_image_with_aspect_ratio(image, size)

    if rgb:
        img_rgb = list(image.getdata())
        for rgb_pixel in img_rgb:
            try:
                for rgb_point in rgb_pixel:
                    img_data.append(rgb_point)
            except:
                raise ValueError("Color argument may not correspond to input image.")
    else:
        img_greyscale = image.convert("L")
        for row in range(0, image.height):
            for col in range(0, image.width):
                img_data.append(img_greyscale.getpixel((col, row)))
    out = {
        "color": rgb,
        "data": zlib.compress(bytes(img_data)),
        "width": image.width,
        "height": image.height,
    }
    return out


def convert_imagefile_to_Image(imfile, rgb=True):
    """
    Converts an image_file (e.g., .jpg) to an ImageData object.
    """
    img = Image.open(imfile, mode="r")
    out = convert_image_to_Image(img, rgb)
    return out


def save_image(image, outfile):
    """
    Saves an PIL.Image object into a file.
    """
    image.save(outfile, format="PNG")
