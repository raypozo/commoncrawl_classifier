#!/bin/bash
#***************************************************
#this script reads from arguments variable $1 a list of urls. 
#downloads each url, uncompresses and extract articles using wikiextractor 
#usage: dowload_everything_wiki_urls.sh [list_urls_to_download]
#Example Command: bash dowload_everything_wiki_urls.sh list_of_urls/wikipedia_urls_output.txt
# Example 2: bash download_everything_wiki_urls.sh langURL.txt
#Example Results: folder extracted.[language] with articles processed
#***************************************************
# IFS='' (or IFS=) prevents leading/trailing whitespace from being trimmed.
# -r prevents backslash escapes from being interpreted.
# || [[ -n $url ]] prevents the last url from being ignored if it doesn't end with a \n 
#   (since read returns a non-zero exit code when it encounters EOF).
#size of sampled file
size=1000000K #1GB
size2=1000000000
#size=100K #1
while IFS='' read -r url || [[ -n "$url" ]]; do
    echo "======================================="
    now=$(date +"%T")
    echo "Current time : $now"
    echo "URLs provided by file: $1"
    echo "Downloading $url"
    re="(.*).org/([a-z_]+)wiki/(.*)"
    if [[ $url =~ $re ]]; then 
        lang=${BASH_REMATCH[2]};    
    fi
    ##file_name=$(python obtain_languaje_from_url.py $url 2)
    ##echo $file_name
#DOWLOADING .GZ FILE
    #if you dowload gzip files, first need to decommpress the file before passing to wikiExtractor
    #gzip -d compressed.gz -c > current.xml
    #wget $url -O compressed.gz
    #python  wikipedia_articles_extractor/WikiExtractor.py current.xml -b 1M -o processed.$lang 
    #rm current.xml
#DOWLOADING BZ2 FILE    
    echo "---------------------------------------"
    wget $url -O compressed.$lang.bz2
    echo "---------------------------------------"
    
    echo "Finished downloading $lang language"
    #lang=$(python obtain_languaje_from_url.py $url 1)
    # echo "Uncompressing compressed.bz2 file, $lang language"
    # bunzip2 -c -k "compressed.$lang.bz2" > $lang.xml
    
    # #check if file exist
    # if [ -f $lang.xml ]; then
    #     size_current=$(wc -c < $lang.xml)
    #     echo "$lang.xml size is $size_current"
    #     #rm compressed.$lang.bz2
    #     echo "Sampling uncompresses file to $size2"
    #     head -c $size2 $lang.xml>sample.$lang.xml
    #     echo "File sample.$lang.xml has been created"
    #     python  wikiextractor/WikiExtractor.py sample.$lang.xml -b 100M -o wp-data/$lang -q 
    #     echo "WikiExtractor completed"
    #     #rm sample.$lang.xml
    # fi
    # #rm current.$lang.xml   

now=$(date +"%T") 
echo "I am done, Bye bye \n $now"
done < "$1"