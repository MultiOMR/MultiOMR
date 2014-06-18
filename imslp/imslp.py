#!/home/alex/anaconda/bin/python

from wikitools import (wiki, category)
import re
import json

site = wiki.Wiki("http://imslp.org/api.php")

catname = "Category:Mozart,_Wolfgang_Amadeus"
cat = category.Category(site, catname)

for p in cat.getAllMembersGen(namespaces=[0]):
    markup = p.getWikiText()
    print(p.title)
    fileinfos = re.findall('{{\s*#fte:imslpfile[\s\n]*((?:\|+.*\n)*)}}', markup)
    for (n, fileinfo) in enumerate(fileinfos):
        print(str(n) + ":")
        fields = re.findall('\|(.*?)\s*=\s*(.*)', fileinfo)
        fs = []
        h = {'files': fs}
        for (k, v) in fields:
            m = re.search('(.*?)\s*([0-9]+)$', k)
            if m:
                file_field = m.group(1)
                file_n = int(m.group(2))
                while len(fs) < file_n:
                    fs.append({})
                fs[file_n-1][file_field] = v
            else:
                h[k] = v
        print json.dumps(h)
        break
    print("")
    break
    
