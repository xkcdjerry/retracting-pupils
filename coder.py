"""A library that handles writing/reading bytes from an image."""
import image


def encode(r, g, b, n):
    return (r&0b11111000 |  (n & 0b00000111),
            g&0b11111000 | ((n & 0b00111000) >> 3),
            b&0b11111100 | ((n & 0b11000000) >> 6))

def decode(r, g, b):
    return ( (r & 0b00000111) +
            ((g & 0b00000111) << 3)+
            ((b & 0b00000011) << 6))


class ImageFile:
    def __init__(self, img: image.RGBImage):
        self.img = img
        self.pos = 0

    def seek(self, pos):
        self.pos = pos

    def tell(self):
        return self.pos

    def write(self, b):
        for i in b:
            self._writechar(i)

    def read(self, n):
        return bytes(self._readchar() for i in range(n))

    def _writechar(self, n):
        r, g, b = self.img.get(self.pos)
        self.img.set(self.pos, encode(r, g, b, n))
        self.pos += 1

    def _readchar(self):
        val = decode(*self.img.get(self.pos))
        self.pos += 1
        return val

    @property
    def size(self):
        return self.img.height*self.img.width

class EncodedImageFile(ImageFile):
    def __init__(self, img, key: int):
        self.key = key
        super().__init__(img)

    def _writechar(self, n):
        super()._writechar((n + self.key) % 256)

    def _readchar(self):
        return (super()._readchar() - self.key) % 256
    
        
