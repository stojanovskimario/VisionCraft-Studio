from PIL import Image, ImageFilter, ImageDraw, ImageFont


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

def add_text(input_path, output_path, text, x, y):
    image = Image.open(input_path)

    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text(
        (x, y),
        text,
        fill="white",
        font=font
    )

    image.save(output_path)

add_text(
    "../test_images/photo.jpg",
    "../test_images/photo_text.jpg",
    "VisionCraftStudio",
    50,
    50
)