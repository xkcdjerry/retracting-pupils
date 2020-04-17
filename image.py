"""A wrapper around PIL.Image"""
import PIL.Image as image

class RGBImage:
    def __init__(self,fname):
        self._img=image.open(fname).convert("RGB")

    def __setitem__(self,xy,val):
        self._img.putpixel(xy,val)

    def __getitem__(self,xy):
        return self._img.getpixel(xy)

    def get(self,n):
        """get the n th pixel, counting left to right and up to down."""
        return self[divmod(n,self.height)]

    def set(self,n,val):
        """set the n th pixel to val, counting left to right and up to down."""
        self[divmod(n,self.height)]=val

    def save(self,fname):
        self._img.save(fname)

    def resize(self, size):
        self._img = self._img.resize(size)

    @property
    def height(self):
        return self._img.height

    @property
    def width(self):
        return self._img.width

