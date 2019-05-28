from PIL import Image

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

def fromColor(color):
    return Image.new('RGB', SIZE, color=color)

def fromString(string, size=SIZE):
    image = Image.new('RGB', size)

    w, h = size
    for y in range(h):
        for x in range(w):
            idx = x + y * w
            color = charToTuple(string[idx])
            image.putpixel((x,y), color)

    return image

def charToRawVal(char):
    """
    a-z = 97-122
    ' ' = 32
    .   = 46
    ,   = 44
    """
    if char == ',':
        val = 26
    elif char == '.':
        val = 27
    elif char == ' ':
        val = 28
    else:
        val = ord(char) - 97

    # Range is now 0-28
    # Scale this to 0x0-0xFFFFFF
    maximum = int(0xFFFFFF)
    factor = maximum // 28
    raw_color = val * factor

    return raw_color

def charToHex(char):

    raw_color = charToRawVal(char)
    return f'#{raw_color:06x}'

def charToTuple(char):
    """
    Bitwise and? Seriously?
    There's gotta be an easier way, but this gets the job done...
    """
    raw = charToRawVal(char)
    r_val = (raw & 0xff0000) // 0x10000
    g_val = (raw & 0x00ff00) // 0x100
    b_val = raw & 0xff

    return (r_val, g_val, b_val)
