'''
Returns the links for all wikipedias specified in the <wikipedia-list> parameter 
that have size smaller than the threshold specified.
Result stored in the outfile name specified

Example Command: python get_list_urls_wikipedia.py wikipedia_list.txt 100000 langURL.txt
Example Result: 
Pinged 296 wikis (294 ok, 2 errors). Total size 55621 MB. Selected size 55621 MB.
'''

import requests
import sys

def make_dump_url(lang):
    # this link is currently not working by Oct 2017
    # return "https://dumps.wikimedia.org/{0}wiki/latest/{0}wiki-latest-pages-articles-multistream.xml.bz2".format(lang)
    return "https://dumps.wikimedia.org/{0}wiki/latest/{0}wiki-latest-pages-articles.xml.bz2".format(lang)
    # return "https://dumps.wikimedia.org/other/wikibase/wikidatawiki/20171009/wikidata-20171009-all.json.bz2".format(lang)

if len(sys.argv) != 4:
    print("Usage: {} <wikipedia-list> <threshold (MB)> <outfile>".format(sys.argv[0]))
    sys.exit(0)

threshold = float(sys.argv[2])

total_size = 0
selected_size = 0
total_wikis = 0
errors = 0

with open(sys.argv[1], 'r') as wikipedia_list, open(sys.argv[3], 'w') as outfile:
    for line in wikipedia_list:
        lang = line.strip()
        if lang == "":
            break
        if not line:
            continue

        total_wikis += 1
        r = requests.head(make_dump_url(lang))
        if not r.ok:
            errors += 1
            print "Could not download dump for", lang
        else:
            size = int(r.headers['Content-Length'])/(1024*1024)
            if size <= threshold:
                selected_size += size
                print "Cheking", lang
                outfile.write('{}\n'.format(make_dump_url(lang)))
            total_size += size

print "Pinged {} wikis ({} ok, {} errors). Total size {} MB. Selected size {} MB.".format(total_wikis, total_wikis-errors, errors, int(total_size), int(selected_size))
print "Links for each language stored in {0}".format(sys.argv[3])

