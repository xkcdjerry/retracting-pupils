import sys
import os

import api

def exit_with(s):
    sys.stderr.write(s)
    raise SystemExit

def main():

    # --------parse---------
    args = sys.argv.copy()
    key = None
    if '--key' in args:
        # deal with the key
        index = args.index('--key')
        key = args[index+1]
        try:
            key = int(key)
            if key>=256:
                raise ValueError
        except ValueError:
            exit_with("Error: key isn't an integer from 0 to 255")
        args[index:index+2]=[]

    # check and unpack
    if len(args) != 4 or args[1] not in ("encode", "decode"):
        exit_with("Usage: %s (encode|decode) filename imagename \
[--key k]" % os.path.basename(args[0]))
    command, filename, imagename = args[1:]
    
    # ----------process--------
    # try to open the image
    try:
        img = api.open(imagename)
    except FileNotFoundError:
        exit_with('image file "%s" does not exist' % imagename)
    
    if command == "encode":
        # handle the files via EAPF
        try:
            fin = open(filename, 'rb')
        except FileNotFoundError:
            exit_with('data file "%s" does not exist' % filename)

        try:
            api.dump(fin, img, key=key)
        except ValueError as e:
            # some error with the file size
            exit_with(e.args[0])

        dirname, fname = os.path.split(imagename)
        fname = os.path.splitext(fname)[0]+'.png'
        newname = "%s/encoded_%s" % (dirname, fname)
        img.save(newname)

    if command == "decode":
        # handle the output file via EAPF
        try:
            fout = open(filename, 'xb')
        except FileExistsError:
            ans = "-"
            
            while ans.lower()[0] not in ("y", "n"):
                ans = input("File already exists, overwrite? (y/n): ")
            
            if ans == "y":
                fout = open(filename, "wb")
            else:
                raise SystemExit
        try:
            api.load(fout, img, key=key)
        except api.CurruptedError as e:
            # some error with the file not containg data
            # or the key is wrong
            exit_with("""Currupt data: %s
Did you use the wrong key and/or chose the wrong file?""" % e.args[0])


if __name__ == "__main__":
    main()
            
        
        
    
