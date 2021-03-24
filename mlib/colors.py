def getIfromRGB(rgb : tuple) -> int:
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint

def hex_to_rgb(value: str) -> tuple:
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def get_main_color(img_url: str) -> tuple:
    from PIL import ImageFile
    import urllib, requests
    file = urllib.request.urlopen(urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla'}))#/JustCheckingImgSize'}))
    
    p = ImageFile.Parser()

    while 1:
        s = file.read(1024)
        if not s:
            break
        p.feed(s)

    im = p.close()
    try:
        return im.getpixel((0, 0))
    except:
        return 0,0,0

def getsizes(uri: str) -> tuple:
    from PIL import ImageFile
    import urllib, requests
    # get file size *and* image size (None if not known)
    try:
        file = urllib.request.urlopen(uri)
    except:
        try:
            file = urllib.request.urlopen(urllib.request.Request(uri, headers={'User-Agent': 'Mozilla'}))#/JustCheckingImgSize'}))
        except:
            return (0, (0,0))
    size = file.headers.get("content-length")
    if size: 
        size = int(size)
    p = ImageFile.Parser()
    while True:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
    file.close()
    return(size, None)

def buffered_image(img: bytes) -> str:
    from io import BytesIO
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()
