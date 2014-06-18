#!/usr/bin/python

#import PythonMagick
from subprocess import call
import os,sys

source = sys.argv[1]

(path, fn) = os.path.split(source)
(name, ext) = os.path.splitext(fn)
dest = os.path.join(path, name + "-noisy" + ext)

# img = PythonMagick.Image(fn)
# seems to be no way of passing a noisetype parameter through..
# img.addNoise("Laplacian")
# img.save(dest)

call(["/usr/bin/convert", source, "+noise", "Poisson", dest])

