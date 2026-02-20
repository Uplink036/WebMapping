import pytest
import math
from PIL import Image, ImageDraw, ImageFont

pytest.skip("Testing logic, not code", allow_module_level=True)

WIDTH, HEIGHT = 1920, 1080

def black_image() -> Image:
    image = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0),"1920x1080",(255,255,255))
    return image

def white_image() -> Image:
    image = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0),"1920x1080",(0,0,0))
    return image

def rainbow_image() -> Image:
    pass

def stich_images(image_one: Image, image_two: Image):
    max_width = WIDTH
    max_height = HEIGHT
    number_of_images = 2

    image_sheet = Image.new("RGB", (max_width, max_height*number_of_images))

    for (i, image) in enumerate([image_one, image_two]):
        image_sheet.paste(image, (
            0,
            max_height * i
        ))
    return image_sheet

def unstitch_image(image: Image) -> list[Image]:
    max_width = WIDTH
    max_height = HEIGHT

    image_width, image_height = image.size[0], image.size[1]
    new_images = math.ceil(image_height/max_height)
    images = [image.crop((
        0, max_height*i,
        max_width, max_height*(i+1)

    )) for i in range(0, new_images)]
    return images


@pytest.mark.parametrize("image", [black_image(), white_image()])
def test_generate_image(image: Image) -> None:
    image_width, image_height = image.size[0], image.size[1]
    assert (image_width, image_height) == (WIDTH, HEIGHT)
    image.save("a_text.png")

@pytest.mark.parametrize("images", [[black_image(), white_image()]])
def test_stitch_images(images: list[Image]) -> None:
    assert len(images) == 2
    stichted = stich_images(images[0], images[1])
    image_width, image_height = stichted.size[0], stichted.size[1]
    assert (image_width, image_height) == (WIDTH, HEIGHT*2)

@pytest.mark.parametrize("images", [[black_image(), white_image()]])
def test_unstitch_image(images):
    assert len(images) == 2
    stichted = stich_images(images[0], images[1])
    unstiched = unstitch_image(stichted)
    assert list(unstiched[0].getdata()) == list(images[0].getdata())
    assert list(unstiched[1].getdata()) == list(images[1].getdata())
