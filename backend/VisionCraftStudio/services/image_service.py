from PIL import Image, ImageFilter


def grayscale(input_path, output_path):
    image = Image.open(input_path)
    gray = image.convert("L")
    gray.save(output_path)


input_path = "../test_images/photo.jpg"
output_path = "../test_images/photo_gray.jpg"

grayscale(input_path, output_path)

def crop_image(input_path, output_path, left, top, right, bottom):
    image = Image.open(input_path)
    cropped = image.crop((left, top, right, bottom))
    cropped.save(output_path)

crop_image(
    "../test_images/photo.jpg",
    "../test_images/photo_crop.jpg",
    100,
    100,
    500,
    500
)

def rotate_image(input_path, output_path, angle):
    image = Image.open(input_path)

    rotated = image.rotate(angle, expand=True)

    rotated.save(output_path)

rotate_image(
    "../test_images/photo.jpg",
    "../test_images/photo_rotated.jpg",
    90
)

def blur_image(input_path, output_path, radius=5):
    image = Image.open(input_path)

    blurred = image.filter(ImageFilter.GaussianBlur(radius))

    blurred.save(output_path)

blur_image(
    "../test_images/photo.jpg",
    "../test_images/photo_blur.jpg",
    10
)