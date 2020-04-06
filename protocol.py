"""A mod to handle dump/load from images"""

import hashlib
import io

import coder

HASHSIZE = 32
LENTHSIZE = 16   # 64bit unsigned int (to record file size)
CHUNKSIZE = 4096
HEADSIZE = HASHSIZE*2 + LENTHSIZE
ORDER = 'big'


class CurruptedError(ValueError):
    """Currupt data or hash."""
    pass

def dumps(b, fimg):
    f = io.BytesIO(b)
    dump(f,fimg)

def loads(fimg):
    f=io.BytesIO()
    load(f,fimg)
    f.seek(0)
    return f.read()

def dump(fin, fimg: coder.ImageFile):

    # write body while recoding the hash and lenth
    size = 0
    digest = hashlib.sha256()
    fimg.seek(HEADSIZE)
    for b in iter(lambda: fin.read(CHUNKSIZE), b''):
        size+=len(b)
        digest.update(b)
        if size+HEADSIZE > fimg.size:
            raise ValueError("File too big to be packed into image.")
        elif size> 256**LENTHSIZE:
            raise ValueError("Filesize too big to be packed into 64bit \
unsigned int")
        fimg.write(b)

    # write the head
    fimg.seek(0)
    size_as_bytes = size.to_bytes(LENTHSIZE, ORDER, signed = False)
    fimg.write(size_as_bytes)
    fimg.write(hashlib.sha256(size_as_bytes).digest())
    fimg.write(digest.digest())

def load(fout, fimg: coder.ImageFile):

    # read file size
    size_as_bytes = fimg.read(LENTHSIZE)
    size_hash_excepted = hashlib.sha256(size_as_bytes).digest()
    size_hash_got = fimg.read(HASHSIZE)
    if size_hash_excepted != size_hash_got:
        raise CurruptedError("Currupt size(excepted hash different from \
got hash)")
    size = int.from_bytes(size_as_bytes, ORDER, signed=False)
    if size + HEADSIZE>fimg.size:
        raise CurruptedError("Currupt size(size to big to be fit into image)")

    # read hash and body
    hash_excepted = fimg.read(HASHSIZE)
    digest = hashlib.sha256()
    
    for i in range(size//CHUNKSIZE):
        chunk = fimg.read(CHUNKSIZE)
        digest.update(chunk)
        fout.write(chunk)
    
    chunk = fimg.read(size%CHUNKSIZE)
    digest.update(chunk)
    fout.write(chunk)

    hash_got = digest.digest()
    if hash_excepted != hash_got:
        raise CurruptedError("Currupt data(excepted hash different from \
got hash)")
    
