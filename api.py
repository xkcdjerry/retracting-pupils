import coder
import image
import protocall as call

CurruptedError = call.CurruptedError
def _getfile(img: image.RGBImage, key=None):
    if key is None:
        return coder.ImageFile(img)
    else:
        return coder.EncodedImageFile(img, key)

def open(fname):
    return image.RGBImage(fname)

def dump(fin, img: image.RGBImage, *, key=None):
    call.dump(fin, _getfile(img, key))

def dumps(b, img: image.RGBImage, *, key=None):
    call.dumps(b, _getfile(img, key))

def load(fout, img:image.RGBImage, *, key=None):
    call.load(fout, _getfile(img, key))

def loads(img: image.RGBImage, *,  key=None):
    return call.loads(_getfile(img, key))
