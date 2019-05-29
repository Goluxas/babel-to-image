import unittest

from PIL import Image

import babelimage as bi


def tupleToHex(tval):
    return f"#{tval[0]:02x}{tval[1]:02x}{tval[2]:02x}"


class BabelImageTestCase(unittest.TestCase):
    def assertPixelEqual(self, colortup, color):
        """
        Accepts either a hex rgb value or a character which it will first
        convert into a hex rgb value
        """
        if len(color) == 1:
            color = bi.charToHex(color)
        self.assertEqual(tupleToHex(colortup), color)

    def test_assertPixelEqual(self):
        self.assertPixelEqual((0, 0, 0), "#000000")
        self.assertPixelEqual((255, 255, 255), "#ffffff")
        self.assertPixelEqual((109, 182, 216), "#6db6d8")


class TestBabelImageE2E(BabelImageTestCase):
    """
    TDD for Pillow Tutorial
    """

    def setUp(self):
        """
        Expected defaults for the time being
        """
        self.WIDTH = 800
        self.HEIGHT = 600
        self.SIZE = (self.WIDTH, self.HEIGHT)

    def test_tupleToHex(self):
        """
        Sanity test for test helper function
        Converts the tuple-style color value given by PIL's getpixel
        function into a hexadecimal string, for my own convenience.
        """
        colorhex = "#ffff00"
        colortup = (255, 255, 0)

        hval = tupleToHex(colortup)

        self.assertEqual(hval, colorhex)

    def test_generate_image_with_given_color(self):
        color = "#ffffff"

        image = bi.fromColor(color)

        self.assertEqual(image.size, self.SIZE)
        self.assertPixelEqual(image.getpixel((1, 1)), color)

    def test_generate_image_from_string(self):
        test_str = "abcdefghijklmnopqrstuvwxyz., "
        c_colorhex = bi.charToHex("c")
        c_coord = (2, 0)
        size = (4, 7)

        image = bi.fromString(test_str, size)

        self.assertEqual(image.size, size)
        self.assertPixelEqual(image.getpixel(c_coord), c_colorhex)

    def test_generate_image_from_page(self):
        """
        Generate an image using the text from a single page of a Library of Babel book.
        I'll load the page as a fixture, to learn that feature.
        Sample the colors at a couple locations.
        """
        with open("samplepage.txt", "r") as infile:
            image = bi.fromPage(infile)

        self.assertEqual(image.size, (80, 40))
        # 0,0 = t
        # 24, 17 = s
        # 79, 39 = e
        self.assertPixelEqual(image.getpixel((0, 0)), bi.charToHex("t"))
        self.assertPixelEqual(image.getpixel((24, 17)), bi.charToHex("c"))
        self.assertPixelEqual(image.getpixel((79, 39)), bi.charToHex("e"))

    def test_generate_image_from_book(self):
        """
        Start with the transposed landscape method of Joe's.
        eg. Each page as a vertical tile of 40x80, Matrix fill
        Full image is 41x10 tiles, Book fill
        """
        with open("samplebook.txt", "r") as infile:
            image = bi.fromBook(infile)

        self.assertEqual(image.size, (41 * 40, 10 * 80))
        self.assertPixelEqual(image.getpixel((0, 0)), ",")
        self.assertPixelEqual(image.getpixel((0, 79)), "r")
        self.assertPixelEqual(image.getpixel((41 * 40 - 1, 799)), "b")
        # self.assertPixelEqual(image.getpixel((x,y)), 'x')
        # self.assertPixelEqual(image.getpixel((x,y)), 'x')
        # self.assertPixelEqual(image.getpixel((x,y)), 'x')
        # self.assertPixelEqual(image.getpixel((x,y)), 'x')


class TestBabelImageUnit(BabelImageTestCase):
    def test_charToHex(self):
        """
        Converts a lowercase character into an rgb hex
        """
        a_hex = bi.charToHex("a")
        space_hex = bi.charToHex(" ")
        m_hex = bi.charToHex("m")

        self.assertEqual(a_hex, "#000000")
        self.assertEqual(m_hex, "#6db6d8")
        # space isn't pure white because of rounding error
        # but that's okay
        self.assertEqual(space_hex, "#fffff8")

    def test_charToTuple(self):
        a_tup = bi.charToTuple("a")
        space_tup = bi.charToTuple(" ")
        m_tup = bi.charToTuple("m")

        self.assertEqual(a_tup, (0, 0, 0))
        self.assertEqual(space_tup, (255, 255, 248))
        self.assertEqual(m_tup, (109, 182, 216))

    def test_read_page(self):
        with open("samplepage.txt", "r") as infile:
            parsed = bi.read_page(infile)

        self.assertNotIn("\n", parsed)
        self.assertEqual(len(parsed), 40 * 80)

    def test_read_book(self):
        """
        Takes a whole downloaded Babel book and returns a list of pages in
        flat string form, ready to be drawn.
        """
        with open("samplebook.txt", "r") as infile:
            parsed = bi.read_book(infile)

        self.assertEqual(len(parsed), 410)
        self.assertEqual(len(parsed[0]), 80 * 40)
        self.assertNotIn("\n", parsed[0])


class TestDraw(BabelImageTestCase):
    def setUp(self):
        self.size = (4, 4)
        self.teststr = "abcdefghijklmnop"

    def test_draw_book_style(self):
        """
        This could potentially become a complicated function...
        """
        # BOOK style draw
        image = Image.new("RGB", self.size)
        image = bi.draw(image, self.teststr, (0, 0), self.size, "BOOK")

        self.assertEqual(image.size, self.size)
        self.assertPixelEqual(image.getpixel((0, 0)), "a")
        self.assertPixelEqual(image.getpixel((3, 3)), "p")
        self.assertPixelEqual(image.getpixel((3, 1)), "h")
        self.assertPixelEqual(image.getpixel((3, 0)), "d")

    def test_draw_matrix_style(self):
        """
        This fill goes top to bottom, left to right
        """
        image = Image.new("RGB", self.size)

        image = bi.draw(image, self.teststr, (0, 0), self.size, "MATRIX")

        self.assertPixelEqual(image.getpixel((0, 0)), "a")
        self.assertPixelEqual(image.getpixel((0, 3)), "d")
        self.assertPixelEqual(image.getpixel((3, 0)), "m")

    def test_draw_partial_rect(self):
        """
        Try drawing a rectangle smaller than the image
        """
        bgcolor = "#111111"
        image = Image.new("RGB", self.size, bgcolor)
        teststr = "abcd"

        image = bi.draw(image, teststr, (1, 1), (2, 2), "BOOK")

        self.assertPixelEqual(image.getpixel((1, 1)), "a")
        self.assertPixelEqual(image.getpixel((2, 2)), "d")
        self.assertPixelEqual(image.getpixel((3, 1)), bgcolor)
        self.assertPixelEqual(image.getpixel((0, 0)), bgcolor)

    def test_draw_with_unknown_style(self):
        image = Image.new("RGB", self.size)

        with self.assertRaises(bi.UnknownDrawStyleException):
            image = bi.draw(image, self.teststr, (0, 0), self.size, "GOOBLEGOBBLE")


if __name__ == "__main__":
    unittest.main()
