"""
The main class for our imager application.
Date:   November 20, 2019
"""

def _is_pixel(item):
    """
    Returns True if item is a pixel, False otherwise.

    A pixel is a tuple of 3 ints in the range 0..255

    Parameter item: The item to check
    Precondition: NONE (item can be anything)(
    """
    if type(item) != tuple or len(item) != 3:
        return False

    for ii in range(3):
        if type(item[ii]) != int or item[ii] < 0 or item[ii] > 255:
            return False

    return True


def _is_pixel_list(data):
    """
    Returns True if data is a pixel list, False otherwise.

    A pixel list is a 1-dimensional list of pixels where a pixel is a tuple
    of 3 ints in the range 0..255

    Parameter data: The data to check
    Precondition: NONE (data can be anything)
    """
    if type(data) is list:
        for x in range(len(data)):
            if _is_pixel(data[x]) == False:
                return False
        return True
    return False


class Image(object):
    """
    A class that allows flexible access to an image pixel list
    """

    # GETTERS AND SETTERS
    def getData(self):
        """
        Returns a COPY of the image data.

        The image data is a 1-dimensional list of 3-element tuples.  The list
        returned by this method is a copy of the one managed by this object.
        """
        return self._data[:]

    def getWidth(self):
        """
        Returns the image width

        """
        return self._width

    def setWidth(self,value):
        """
        Sets the image width to value, assuming it is valid.

        Parameter value: the new width value
        Precondition: value is a valid width >= 0
        """
        assert type(value) is int
        assert len(self.getData()) % value == 0
        if len(self.getData()) == 0:
            assert value == 0
        else:
            assert value != 0
        assert value * len(self.getData())//value == len(self.getData())

        self._width = value
        self.setHeight(len(self.getData())//self._width)
        self._width = len(self.getData())//self.getHeight()

    def getHeight(self):
        """
        Returns the image height
        """
        return self._height

    def setHeight(self,value):
        """
        Sets the image height to value, assuming it is valid.

        Parameter value: the new height value
        Precondition: value is a valid height >= 0
        """
        if len(self.getData()) == 0:
            height = 0
        else:
            height = value
            assert type(height) is int
            assert len(self.getData()) % height == 0

        self._height = height
        self._width = len(self.getData())//height
        assert self._width * value == len(self.getData())

    # INITIALIZER
    def __init__(self, data, width):
        """
        Initializes an Image from the given pixel list.

        Parameter data: The image data as a pixel list
        Precondition: data is a pixel list

        Parameter width: The image width
        Precondition: width is an int > 0 and evenly divides the length of pixels
        """
        assert _is_pixel_list(data)
        self._data = data
        self.setWidth(width)
        self.setHeight(len(self.getData())//width)

    # OPERATOR OVERLOADING
    def __len__(self):
        """
        Returns the number of pixels in this image

        This special method supports the built-in len function.
        """
        return len(self.getData())

    def __getitem__(self, pos):
        """
        Returns the pixel at the given position.

        The value returned is a 3-element tuple (r,g,b).

        Parameter pos: The position in the pixel list
        Precondition: pos is an int and a valid position >= 0 in the pixel list.
        """

        assert type(pos) is int
        assert pos >= 0 and pos < len(self._data)
        return self._data[pos]

    def __setitem__(self, pos, pixel):
        """
        Sets the pixel at the given position to the given value.

        Parameter pos: The position in the pixel list
        Precondition: pos is an int and a valid position >= 0 in the pixel list.

        Parameter pixel: The pixel value
        Precondition: pixel is a 3-element tuple (r,g,b) of ints in 0..255
        """
        assert type(pos) is int
        assert pos >= 0 and pos < len(self.getData())
        assert _is_pixel(pixel)

        list = self._data
        list[pos] = pixel

    # TWO-DIMENSIONAL ACCESS METHODS
    def getPixel(self, row, col):
        """
        Returns a copy of the pixel value at (row, col)

        The value returned is a 3-element tuple (r,g,b).

        Parameter row: The pixel row
        Precondition: row is an int >= 0 and < height

        Parameter col: The pixel column
        Precondition: col is an int >= 0 and < width
        """
        assert (type(row) is int) and (row >= 0) and (row < self.getHeight())
        assert (type(col) is int) and (col >= 0) and (col < self.getWidth())

        return self.getData()[row*self.getWidth() + col%self.getWidth()]

    def setPixel(self, row, col, pixel):
        """
        Sets the pixel value at (row, col) to (a copy of) pixel

        Parameter row: The pixel row
        Precondition: row is an int >= 0 and < height

        Parameter col: The pixel column
        Precondition: col is an int >= 0 and < width

        Parameter pixel: The pixel value
        Precondition: pixel is a 3-element tuple (r,g,b) of ints in 0..255
        """
        assert (type(row) is int) and (row >= 0) and (row < self.getHeight())
        assert (type(col) is int) and (col >= 0) and (col < self.getWidth())
        assert _is_pixel(pixel)

        list = self._data
        copy_pixel = pixel
        list[row*self.getWidth() + col%self.getWidth()] = copy_pixel

    def __str__(self):
        """
        Returns: The string representation of this image.

        The string should be displayed as a 2D list of pixels in row-major
        order. For example, suppose the image data is

            [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (128, 0, 0), (0, 128, 0)]

        """
        string_rep = '['
        a = 0
        for x in range(self.getHeight()):
            string_rep += '['
            for y in range(self.getWidth()):
                string_rep += str(self.__getitem__(a))
                if y == self.getWidth()-1 :
                    string_rep += ']'
                    if x!=(self.getHeight()) - 1 :
                        string_rep += ','
                else:
                    string_rep += ', '
                if (a<len(self.getData())-1):
                    a += 1
            if x!=(self.getHeight()) - 1 :
                string_rep+= '\n'
        string_rep += ']'

        return string_rep

    # ADDITIONAL METHODS
    def swapPixels(self, row1, col1, row2, col2):
        """
        Swaps the pixel at (row1, col1) with the pixel at (row2, col2)

        Parameter row1: The pixel row to swap from
        Precondition: row1 is an int >= 0 and < height

        Parameter col1: The pixel column to swap from
        Precondition: col1 is an int >= 0 and < width

        Parameter row2: The pixel row to swap to
        Precondition: row1 is an int >= 0 and < height

        Parameter col2: The pixel column to swap to
        Precondition: col2 is an int >= 0 and < width
        """
        temp = self.getPixel(row1,col1)
        self.setPixel(row1,col1,self.getPixel(row2,col2))
        self.setPixel(row2,col2,temp)

    def copy(self):
        """
        Returns a copy of this image object.
        """
        copy_obj = Image(self.getData(),self.getWidth())
        copy_obj._data = self.getData()[:]
        copy_obj._width = self.getWidth()
        return copy_obj
