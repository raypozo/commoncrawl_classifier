#!/bin/bash
#***************************************************
#this script reads from arguments variable $1 a list of languages. 
#Copies each language AA folder into HDFS
#usage: copy_hdfs.sh lang_list.txt

#***************************************************
echo "Languages provided by file: $1"
hadoop fs -mkdir decompressed
while IFS='' read -r lang ; do
    echo "======================================="
    now=$(date +"%T")
    echo "Current time : $now"
    echo "Copying language $lang to HDFS"
	hadoop fs -mkdir decompressed/"$lang"
	hadoop fs -mkdir decompressed/"$lang"/AA
	hadoop fs -put decompressed2/"$lang"/AA/wiki_0* decompressed/"$lang"/AA
echo "Copy process complete"
done < "$1"