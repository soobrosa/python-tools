#!/usr/bin/env py

# examples
#
# Wordpress posts -- wp_posts 0,3,4,5
#
# Scuttle bookmarks-- scBookmarks 0,6,7,8 (0)
# Scuttle tags -- scCategories 0,1,2 (1)
# join on ()

import sys
import re

log = sys.stderr.write

# regex a .csv line via http://stackoverflow.com/questions/2212933/python-regex-for-reading-csv-like-rows
r = re.compile(r'''\s*([^,"']+?|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')\s*(?:,|$)''', re.VERBOSE)

def convert(filename, table, fields):
    prefix = '/*!40000 ALTER TABLE `' + table + '` DISABLE KEYS */;'
    postfix = '/*!40000 ALTER TABLE `' + table + '` ENABLE KEYS */;'
    found = False
    
    input_file = open(filename, 'r')
    for line in input_file:
        if found:
            if line.startswith(postfix):
                found = False
            else:
                if line.startswith('INSERT INTO'):
                    line = line.split('` VALUES (')[1]
                items = line.strip().split('),(')
                for item in items:
                    if item.endswith(');'):
                        item  = item.split(');')[0]
                    columns = r.findall(item)
                    output = []
                    for field in fields:
                        output.append(columns[field].strip("'"))
                    print '\t'.join(output)
        if not found and line.startswith(prefix):
            found = True
    input_file.close()
        
if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        table = sys.argv[2]
        fields = eval(sys.argv[3])

    except IndexError, e:
        log("Usage: mysql_to_tsv filename table fields\n")
        raise SystemExit(1)

    convert(filename, table, fields)