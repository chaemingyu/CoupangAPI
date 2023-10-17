from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys

def make_thumb(path, title, gradient_magnitude=1.):

    try :
        im = Image.open(path+".jpg")
    except  :
        try :
            im = Image.open(path+".png")
        except :
            im = Image.open(path+".jpeg")
    im = resize(im)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    width, height = im.size
    gradient = Image.new('L', (1, 255), color=0xFFFFFF)
    for y in range(255):
        gradient.putpixel((0, y-255), y)
    alpha = gradient.resize(im.size)
    black_im = Image.new('RGBA', (width, height), color=0)  # i.e. black
    black_im.putalpha(alpha)
    gradient_im = Image.alpha_composite(im, black_im)
    gradient_im = set_tile(gradient_im)
    result_im = set_text(gradient_im, title)
    result_im.save("result/"+title.split("\n")[1]+'.png', 'PNG')

def set_text(im, text) :
    text1, text2 = text.split("\n")
    draw = ImageDraw.Draw(im)
    fontsize = 1
    img_fraction = 0.85
    option = int(input("[Input]텍스트 옵션(1:감성,2:마케팅) : "))
    font = ImageFont.truetype("fonts/KimNamyun.ttf", fontsize)
    if option == 2 :
        font = ImageFont.truetype("fonts/GmarketSansTTFMedium.ttf", fontsize)
        img_fraction = 1.0
    while font.getsize(text)[0] < img_fraction * im.size[0] :
        fontsize += 1
        if option == 1 :
            font = ImageFont.truetype("fonts/KimNamyun.ttf", fontsize)
        elif option == 2:
            font = ImageFont.truetype("fonts/GmarketSansTTFMedium.ttf", fontsize)
        #print("폰트 사이즈 : " , font.getsize(text)[0],img_fraction * im.size[0])

    fontsize-=1
    width, height = im.size
    w, h = font.getsize(text1)
    w2, h2 = draw.textsize(text2, font=font)
    if option == 1:
        font2 = ImageFont.truetype("fonts/KimNamyun.ttf", fontsize)
        draw.text((int((width - w) / 2), int((height - h) / 2) - h2 / 2), text1, (255, 255, 255), font=font, align="center")
        draw.text((int((width - w2) / 2), int((height - h2) / 2) + h2 / 2), text2, (255, 199, 21), font=font2, align="center")
    if option == 2 :
        font2 = ImageFont.truetype("fonts/GmarketSansTTFBold.ttf", fontsize)
        draw.text((int((width - w) / 2), int((height - h) / 2) - h2 /2), text1, (255, 255, 255), font=font, align="center")
        draw.text((int((width - w2) / 2), int((height - h2) / 2) + h2 / 2), text2, (255, 199, 21), font=font2, align="center")

    return im

def set_tile(im) :
    w, h = im.size
    tile = Image.open("res/tile.png")
    tile_w, tile_h = tile.size
    start_x = int ( (w - tile_w)/2)
    start_y = int ( (h - tile_h)/2)
    im.paste(tile,( start_x,start_y),tile.convert('RGBA'))
    return im

def resize(im) :
    width, height = im.size
    if width > height :
        gap = width - height
        left = gap / 2
        top = 0
        im = im.crop((left, top, height + (gap/2) , top + height))
    elif width < height :
        gap = height - width
        left = 0
        top = gap / 2
        im = im.crop((left, top, width, top + width))
    im = im.resize((600,600))
    return im