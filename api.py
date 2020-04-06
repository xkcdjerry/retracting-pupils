import coder
import image
import protocol as col
from protocol import CurruptedError


def _getfile(img: image.RGBImage, key=None):
    if key is None:
        return coder.ImageFile(img)
    else:
        return coder.EncodedImageFile(img, key)

def open(fname):
    return image.RGBImage(fname)

def dump(fin, img: image.RGBImage, *, key=None):
    col.dump(fin, _getfile(img, key))

def dumps(b, img: image.RGBImage, *, key=None):
    col.dumps(b, _getfile(img, key))

def load(fout, img:image.RGBImage, *, key=None):
    col.load(fout, _getfile(img, key))

def loads(img: image.RGBImage, *,  key=None):
    return col.loads(_getfile(img, key))
