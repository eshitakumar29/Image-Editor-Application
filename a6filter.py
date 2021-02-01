"""
Image processing methods for the imager application.
Date:   November 20, 2019
"""
import a6editor


class Filter(a6editor.Editor):
    """
    A class that contains a collection of image processing methods
    """

    def invert(self):
        """
        Inverts the current image, replacing each element with its color complement
        """
        current = self.getCurrent()
        for pos in range(len(current)):
            rgb = current[pos] 
            red   = 255 - rgb[0]
            green = 255 - rgb[1]
            blue  = 255 - rgb[2]
            rgb = (red,green,blue)
            current[pos] = rgb

    def transpose(self):
        """
        Transposes the current image
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())

        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(col,row))

    def reflectHori(self):
        """
        Reflects the current image around the horizontal middle.
        """
        current = self.getCurrent()
        for h in range(current.getWidth()//2):
            for row in range(current.getHeight()):
                k = current.getWidth()-1-h
                current.swapPixels(row,h,row,k)

    def rotateRight(self):
        """
        Rotates the current image left by 90 degrees.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())

        for row in range(current.getHeight()):
            for col in range(current.getWidth()):  
                current.setPixel(row,col,original.getPixel(original.getHeight()-col-1,row))

    def rotateLeft(self):
        """
        Rotates the current image left by 90 degrees.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())

        for row in range(current.getHeight()): 
            for col in range(current.getWidth()): 
                current.setPixel(row,col,original.getPixel(col,original.getWidth()-row-1))

    def reflectVert(self):
        """
        Reflects the current image around the vertical middle.
        """
        current = self.getCurrent()
        for h in range(current.getWidth()):  
            for row in range(current.getHeight()//2):
                k = current.getHeight()-1-row
                current.swapPixels(row,h,k,h)

    def monochromify(self, sepia):
        """
        Converts the current image to monochrome (greyscale or sepia tone).

        If `sepia` is False, then this function uses greyscale. It removes all
        color from the image by setting the three color components of each
        pixel to that pixel's overall brightness, defined as

            brightness = 0.3 * red + 0.6 * green + 0.1 * blue.

        If sepia is True, it makes the same computations as before but sets
        green to 0.6 * brightness and blue to 0.4 * brightness.

        Parameter sepia: Whether to use sepia tone instead of greyscale.
        Precondition: sepia is a bool
        """
        current = self.getCurrent()
        for pos in range(len(current)):
            rgb = current[pos]
            brightness=(0.3*rgb[0])+(0.6*rgb[1])+(0.1*rgb[2])
            if(sepia==False):
                rgb=(int(brightness),int(brightness),int(brightness))
            if(sepia==True):
                rgb=(int(brightness),int(0.6*brightness),int(0.4*brightness))
            current[pos] = rgb

    def jail(self):
        """
        Puts jail bars on the current image

        The jail should be built as follows:
        * Put 3-pixel-wide horizontal bars across top and bottom,
        * Put 4-pixel vertical bars down left and right, and
        * Put n 4-pixel vertical bars inside, where n is
          (number of columns - 8) // 50.
          
        The n+2 vertical bars should be as evenly spaced as possible.
        """
        color=(255,0,0)
        current = self.getCurrent()
        self._drawHBar(0,color)
        self._drawHBar((current.getHeight()-3),color)
        self._drawVBar(0,color)
        self._drawVBar((current.getWidth()-4),color)
        n=(current.getWidth()-8)//50
        space_left=current.getWidth()-8-4*n
        distance=(space_left/(n+1))
        for x in range(1,n+1):
            self._drawVBar(int(round(x*(distance+4))),color)

    def vignette(self):
        """
        Modifies the current image to simulates vignetting (corner darkening).

        Vignetting is a characteristic of antique lenses. This plus sepia tone
        helps give a photo an antique feel.
        """
        current=self.getCurrent()
        height=current.getHeight()
        width=current.getWidth()
        h2=((height/2)*(height/2))+((width/2)*(width/2))
        for x in range(int(width)):
            for y in range(int(height)):
                d2=((x-(width/2))*(x-(width/2)))+((y-(height/2))*(y-(height/2)))
                val=1-(d2/h2)
                col=current.getPixel(x,y)
                red=(col[0])*val
                green=(col[1])*val
                blue=(col[2])*val
                current.setPixel(x,y,(int(red),int(green),int(blue)))

    # HELPER METHODS
    def _drawHBar(self, row, pixel):
        """
        Draws a horizontal bar on the current image at the given row.

        This method draws a horizontal 3-pixel-wide bar at the given row
        of the current image. This means that the bar includes the pixels
        row, row+1, and row+2. The bar uses the color given by the pixel
        value.

        Parameter row: The start of the row to draw the bar
        Precondition: row is an int, 0 <= row  &&  row+2 < image height

        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,b,g) of ints in 0..255
        """
        current = self.getCurrent()
        for col in range(current.getWidth()):
            current.setPixel(row,   col, pixel)
            current.setPixel(row+1, col, pixel)
            current.setPixel(row+2, col, pixel)

    def _drawVBar(self,col,pixel):
        """
        Draws a vertical var on the current image at a given column.

        This method draws a vertical 4-pixel-wide bar at the given column
        of the current image. This means that the bar includes the pixels
        row, row+1, row+2, and row+3. The bar uses the color given by the
        pixel value.

        Parameter col: The start of the column to draw the bar
        Precondition: col is an int, 0 <= col and col+3 < image height

        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) of ints in bewteen 0
        and 255
        """
        current = self.getCurrent()
        for row in range(current.getHeight()):
            current.setPixel(row,col,pixel)
            current.setPixel(row,col+1,pixel)
            current.setPixel(row,col+2,pixel)
            current.setPixel(row,col+3,pixel)
