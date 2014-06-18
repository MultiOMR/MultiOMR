#!/home/alex/anaconda/bin/python

from music21 import *
import lxml.etree as ET
import os, sys
from subprocess import call
from tempfile import (mkstemp, NamedTemporaryFile)

def tempfn():
    f = NamedTemporaryFile(delete=False)
    fn = f.name
    f.close()
    return(fn)

def tempf():
    f = NamedTemporaryFile(delete=False)
    return(f)

def audiveris_args(fn_in, fn_out):
    return ["-batch", "-input", fn_in, "-export", fn_out]

def run_scan_webstart(fn_in):
    fn_out = tempfn()

    fh = open("audiveris.jnlp", "r")
    tree = ET.parse(fh)
    fh.close()

    arg_desc = tree.find(".//application-desc")
    for arg in audiveris_args(fn_in, fn_out):
        arg_desc.append(ET.XML("<argument>" + arg + "</argument>\n"))

    tmp_fh = tempf()
    tmp_fn = tmp_fh.name
    tmp_fh.write(ET.tostring(tree))
    tmp_fh.close()
    print("fn: " + tmp_fn)
    call(["javaws", tmp_fn])
    return(fn_out)
    #os.unlink(tmp_fn)

def run_scan_jar(fn_in):
    fn_out = tempfn()
    jarfile = "/home/alex/netbeans/audiveris~hg/dist/audiveris.jar"
    args = ["java", "-Xms2048m", "-Xmx2048m", "-jar", jarfile] + audiveris_args(fn_in, fn_out)
    print("running " + " ".join(args))
    call(args)
    return(fn_out)

# Uses lilypond..
def render_music21(i, o):
    x = converter.parse(i)
    f = x.write(fmt="lily.pdf", fp=o)

def render_musescore(i, o):
    call(["musescore", i, "-o", o])

source = sys.argv[1]
(path, fn) = os.path.split(source)
(name, ext) = os.path.splitext(fn)

cycles = 3
infn = source

for i in range(0,cycles):
    outfn =  name + "-" + str(i)
    outxml = outfn + ".xml"
    outpdf = outfn + ".pdf"
    fn_mxl = run_scan_jar(infn)
    os.rename(fn_mxl, outxml)

    #render_music21(outxml, outpdf)
    render_musescore(outxml, outpdf)
    infn = outpdf
