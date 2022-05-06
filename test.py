from PIL import Image, ImageFont, ImageDraw
from os import getcwd
from io import BytesIO

def create_code_image(code: str):

    path = getcwd()+"/assets/misc/code.png"
    font = getcwd()+'/assets/misc/font.otf'

    f = ImageFont.truetype(font, 95)
    img = Image.open(path, 'r').convert('RGBA')

    ImageDraw.Draw(img).text((250, 430), code, fill=(255,255,255), font=f)
    bytes_ = BytesIO()
    img.save(bytes_, 'PNG')
    bytes_.seek(0)
    return bytes_