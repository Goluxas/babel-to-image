from PIL import Image

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)


def fromColor(color):
    return Image.new("RGB", SIZE, color=color)


def fromString(string, size=SIZE):
    image = Image.new("RGB", size)

    w, h = size
    for y in range(h):
        for x in range(w):
            idx = x + y * w
            color = charToTuple(string[idx])
            image.putpixel((x, y), color)

    return image


def fromPage(pagefp):
    width = 80
    height = 40
    size = (width, height)

    image = Image.new("RGB", size)

    page_str = read_page(pagefp)
    image = draw(image, page_str, (0, 0), size, "BOOK")

    return image


def fromBook(bookfp):
    """
    For now, no options.
    Always draw 41x10 tiles book style
    Each tile is 40x80 drawn matrix style
    """
    size = (40 * 41, 80 * 10)
    w, h = size

    tiles = (41, 10)
    tile_size = (40, 80)
    tile_w, tile_h = tile_size

    image = Image.new("RGB", size, "#111111")

    book = read_book(bookfp)
    for ty in range(tiles[1]):
        for tx in range(tiles[0]):
            page_idx = tx + ty * tiles[0]
            tile_origin = (tx * tile_w, ty * tile_h)
            image = draw(image, book[page_idx], tile_origin, tile_size, "MATRIX")

    return image


class UnknownDrawStyleException(Exception):
    pass


def draw(image, colors, start, size, style):
    width, height = size

    if style == "BOOK":
        """
        Left to right, top to bottom, like letters on a page
        """
        for y in range(height):
            for x in range(width):
                idx = x + y * width
                color = charToTuple(colors[idx])
                image.putpixel((x + start[0], y + start[1]), color)
    elif style == "MATRIX":
        """
        Top to bottom, left to right, _kinda_ like the Matrix
        """
        for x in range(width):
            for y in range(height):
                idx = y + x * height
                color = charToTuple(colors[idx])
                image.putpixel((x + start[0], y + start[1]), color)
    else:
        raise UnknownDrawStyleException

    return image


def read_page(pagefp):
    page_str = "".join([line.replace("\n", "") for line in pagefp])
    return page_str


def read_book(bookfp):
    """
    Reads an entire Babel book, breaks it into pages and returns a list
    of flattened strings ready for draw()
    """
    book = bookfp.readlines()
    # cut title and footer
    book = book[2:-2]
    # book is now in the format where 40 indices in a row are 1 page, then a blank line, repeat
    pages = []
    while len(book) > 0:
        # convert 40 lines into a page
        page = read_page(book[0:40])
        pages.append(page)
        # slice the 40 lines + whitespace line off
        book = book[41:]

    return pages


def charToRawVal(char):
    """
    a-z = 97-122
    ' ' = 32
    .   = 46
    ,   = 44
    """
    if char == ",":
        val = 26
    elif char == ".":
        val = 27
    elif char == " ":
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
    return f"#{raw_color:06x}"


def charToTuple(char):
    """
    Bitwise and? Seriously?
    There's gotta be an easier way, but this gets the job done...
    """
    raw = charToRawVal(char)
    r_val = (raw & 0xFF0000) // 0x10000
    g_val = (raw & 0x00FF00) // 0x100
    b_val = raw & 0xFF

    return (r_val, g_val, b_val)
