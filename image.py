"""A wrapper around PIL.Image"""
import PIL.Image as image

class RGBImage:
    def __init__(self,fname):
        self.img=image.open(fname).convert("RGB")

    def __setitem__(self,xy,val):
        self.img.putpixel(xy,val)

    def __getitem__(self,xy):
        return self.img.getpixel(xy)

    def get(self,n):
        """get the n th pixel, counting left to right and up to down."""
        return self[divmod(n,self.height)]

    def set(self,n,val):
        """set the n th pixel to val, counting left to right and up to down."""
        self[divmod(n,self.height)]=val

    def save(self,fname):
        self.img.save(fname)

    @property
    def height(self):
        return self.img.height

    @property
    def width(self):
        return self.img.width

