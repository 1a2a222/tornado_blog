import glob,os
from PIL import Image

def get_images(path):
    image_urls = glob.glob(path+'/*.jpg')
    return image_urls

def make_thumb(path):
    im = Image.open(path)
    im.thumbnail((200,200))
    name = os.path.basename(path)
    filename,ext = os.path.splitext(name)
    im.save('static/uploads/thumb/{}_{}*{}{}'.format(filename,200,200,ext))