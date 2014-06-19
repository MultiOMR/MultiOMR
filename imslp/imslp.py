#!/home/alex/anaconda/bin/python

from wikitools import (wiki, category)
import re
import json
import sqlite3


site = wiki.Wiki("http://imslp.org/api.php")


db = sqlite3.connect('imslp.db')

field_lookup = {}
file_field_lookup = {}


def to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

def add_dbfields(table, fields):
    c = db.cursor()
    c.execute('''select sql from sqlite_master where tbl_name = ?''', (table,))
    (create,) = c.fetchone()
    fieldlist = re.search(r'\((.*?)\)', create)
    current = re.split(r',\s*', fieldlist.group(1))
    current = map((lambda x: re.sub(r' text$', '', x)), current)
    for field in fields:
        if not field in current:
            db.execute('alter table ' + table + ' add column ' + field + ' text')

def compress(v):
    v = re.sub(r'[^a-zA-Z0-9]', '', v)
    return(v)

def getCat(cat):
    scores = []
    files = []
    # get all the pages in this category
    for p in cat.getAllMembersGen(namespaces=[0]):
        # get the wiki markup
        markup = p.getWikiText()
        print(p.title + " " + "http://imslp.org/wiki/" + p.urltitle)
        #print markup
        # grab the file section
        filesec = re.search('\*+FILES\*{5}(.+?)\*\*\*', markup,flags=re.DOTALL)
        if not filesec:
            print "no file section"
            continue
        # find the subsections inside that
        subsecs = re.findall('===\s*(.*?)\s*===(.*?)$', filesec.group(1),flags=re.DOTALL)
        print("subsecs: %d" % len(subsecs))

        # No sub sections, use the whole file section
        if len(subsecs) == 0:
            subsecs = [("None", filesec.group(1))]

        for m in subsecs:
            scoretype = m[0]
            content = m[1]
            # find the files inside each subsection
            fileinfos = re.findall('{{\s*#fte:imslpfile[\s\n]*((?:\|+.*\n)*)}}', content)
            for (n, fileinfo) in enumerate(fileinfos):
                print(str(n) + ":")
                fields = re.findall('\|+(.*?)[\t ]*=[\t ]*(.*)\n', fileinfo)
                
                # build a dictionary of info for the file
                s = {u'id': p.urltitle,
                     u'scoretype': scoretype, 
                     u'category': catname
                    }
                # extract the key value pairs from the file info and add to the 
                # dict
                for (k, v) in fields:
                    m = re.search('(.*?)\s*(\d+)$', k)
                    if m:
                        file_field = m.group(1)
                        file_field = compress(file_field)
                        file_n = int(m.group(2))
                        f = {}
                        f[u'file_n'] = file_n
                        f[u'score'] = p.urltitle
                        f[file_field] = v
                        files.append(f)
                        file_field_lookup[file_field] = 1
                    else:
                        s[compress(k)] = v
                        field_lookup[compress(k)] = 1
                print json.dumps(s)
                scores.append(s)
    return(scores, files)


db.execute('''create table if not exists score (id text, category text, scoretype text)''')
db.execute('''create table if not exists scorefile (file_n text, score text)''')

catname = "Category:Mozart,_Wolfgang_Amadeus"
cat = category.Category(site, catname)
(scores, files) = getCat(cat)

# Make sure the database has the right columns available..
add_dbfields(u"score", field_lookup.keys())
add_dbfields(u"scorefile", file_field_lookup.keys())

c = db.cursor()
for score in scores:
    c.execute('''select count(*) from score where id = ?''', (score['id'],))
    (n,) = c.fetchone()
    if n == 0:
        columns = map (to_unicode, score.keys())
        values = map((lambda column: to_unicode(score[column])), columns)
        query = "insert into score (" + ", ".join(columns) + ") values (" + (", ".join(["?"] * len(columns))) + ")"
        print("execute " + query + " with " + ",".join(values))
        c.execute(query, values)

for f in files:
    c.execute('''select count(*) from scorefile where score = ? and file_n = ?''', (f['score'], f['file_n']))
    (n,) = c.fetchone()
    if n == 0:
        columns = map (to_unicode, f.keys())
        values = map((lambda column: to_unicode(f[column])), columns)
        query = "insert into scorefile (" + ", ".join(columns) + ") values (" + (", ".join(["?"] * len(columns))) + ")"
        print("execute " + query + " with " + ",".join(values))
        c.execute(query, values)

db.commit()
