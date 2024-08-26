import sys
import re
import codecs
sys.stdout.reconfigure(encoding='ISO-8859-1')

outputFile = codecs.open(sys.argv[2], "w", "ISO-8859-1")

with open(sys.argv[1], 'r', encoding='iso-8859-1') as f:
    hitlist = f.read()

for line in hitlist.split("\n"):
    #[hobo=414088]414088[/hobo]
    search = re.search(r'(.*?)\(([\s\d][\s\d][\s\d]+)\)(.*)', line)
    newline = search.group(1) + '([hobo=' + search.group(2) + ']' + search.group(2) + '[/hobo])' + search.group(3)
    # print(newline)
    outputFile.write((newline + '\n'))

outputFile.close()