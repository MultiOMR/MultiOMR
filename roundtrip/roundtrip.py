#!/usr/bin/python

import lxml.etree as ET
import os
from subprocess import call
from tempfile import mkstemp

def run_scan(fn):
    fh = open("audiveris.jnlp", "r")
    tree = ET.parse(fh)
    fh.close()

    arg_desc = tree.find(".//application-desc")
    for arg in ["-batch", "-input", fn, "-step", "EXPORT", "-export", "/tmp/scan.mxl"]:
        arg_desc.append(ET.XML("<argument>" + arg + "</argument>\n"))

    (tmp_fd, tmp_fn) = mkstemp()
    tmp_fh = os.fdopen(tmp_fd, "w")
    tmp_fh.write(ET.tostring(tree))
    tmp_fh.close()
    print("fn: " + tmp_fn)
    call(["javaws", tmp_fn])
    #os.unlink(tmp_fn)


run_scan("/tmp/music21/tmpIigfOM.pdf")
