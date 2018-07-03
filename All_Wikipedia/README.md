
# Explanation of Code

## The Extract Folder

Contains partial corpus of the warwiki, downloaded by 

```
wget http://download.wikimedia.org/warwiki/latest/warwiki-latest-pages-articles.xml.bz2
python wikiextractor/WikiExtractor.py -cb 250K -o extracted warwiki-latest-pages-articles.xml.bz2
```

stopped after 1.3 million of corpus (17.8 MB) downloaded. Whole warwiki file 3.83 GB in xml format.

Documents from the same language are split into different folders when downloading (AA, AB, AC, ...) with each folder 2 ~ 3 MG. Should merge them together to a file called text.xml using 

```
find extracted -name '*bz2' -exec bzip2 -c {} \; > text.xml
rm -rf extracted
```

For more information and examples for the extractor, please see http://medialab.di.unipi.it/wiki/Wikipedia_Extractor.

## List of Languages

The labels are self-created. Original language names taken from https://en.wikipedia.org/wiki/List_of_Wikipedias.

## get_list_urls_wikipedia.py
get_list_urls_wikipedia.py gets the sizes in MB for all wikipedias specified in the <wikipedia-list> parameter,that overcome a defined threshold <threshold (MB)>
    
<wikipedia-list> is the set of languajes to be dowloaded. In the folder it would be 'wikipedia_list.txt' 
<threshold (MB> is the size in MB that if the url overcomes,our program is not going to download)

Currently get-wikipedia looks in the urls "https://dumps.wikimedia.org/{0}wiki/latest/{0}wiki-latest-pages-articles.xml.bz2" where {0} represents tha lang to be searched

Output is a list of urls that accomplish the mentioned above 

```python get-wikipedia.py wikipedia_list.txt 100 langURL.txt```

### More information about wikimedia
(https://meta.wikimedia.org/wiki/Data_dumps)

## download_everything_wiki_urls.sh
download_everything_wiki_urls.sh reads a list of urls(passed as a parameter). 
downloads each url, uncompresses and extract articles using wikiextractor. 

```dowload_everything_wiki_urls.sh [list_urls_to_download]```

Example Command: ```bash dowload_everything_wiki_urls.sh langURL.txt```

Example Results: folder extracted.[language]/ 
