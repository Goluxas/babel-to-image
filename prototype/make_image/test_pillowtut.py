import unittest
import pillowtut as p

def tupleToHex(tval):
    return f'#{tval[0]:02x}{tval[1]:02x}{tval[2]:02x}'

class TestPillowTutE2E(unittest.TestCase):
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
        colorhex = '#ffff00'
        colortup = (255, 255, 0)

        hval = tupleToHex(colortup)

        self.assertEqual(hval, colorhex)

    def assertPixelEqual(self, colortup, colorhex):
        self.assertEqual( tupleToHex(colortup), colorhex )

    def test_generate_image_with_given_color(self):
        color = '#ffffff'

        image = p.fromColor(color)

        self.assertEqual(image.size, self.SIZE)
        self.assertPixelEqual(image.getpixel((1,1)), color)

    def test_generate_image_from_string(self):
        test_str = 'abcdefghijklmnopqrstuvwxyz., '
        c_colorhex = p.charToHex('c')
        c_coord = (2,0)
        size = (4,7)
        
        image = p.fromString(test_str, size)

        self.assertEqual(image.size, size)
        self.assertPixelEqual(image.getpixel(c_coord), c_colorhex)

    def test_generate_image_from_page(self):
        """
        Generate an image using the text from a single page of a Library of Babel book.
        I'll load the page as a fixture, to learn that feature.
        Sample the colors at a couple locations.
        """
        self.fail('write it!')

class TestPillowTutUnit(unittest.TestCase):
    
    def test_charToHex(self):
        """
        Converts a lowercase character into an rgb hex
        """
        a_hex = p.charToHex('a')
        space_hex = p.charToHex(' ')
        m_hex = p.charToHex('m')

        self.assertEqual(a_hex, '#000000')
        self.assertEqual(m_hex, '#6db6d8')
        # space isn't pure white because of rounding error
        # but that's okay
        self.assertEqual(space_hex, '#fffff8')

    def test_charToTuple(self):
        a_tup = p.charToTuple('a')
        space_tup = p.charToTuple(' ')
        m_tup = p.charToTuple('m')

        self.assertEqual(a_tup, (0,0,0))
        self.assertEqual(space_tup, (255, 255, 248))
        self.assertEqual(m_tup, (109, 182, 216))


if __name__ == '__main__':
    unittest.main()
