#!/bin/bash
#***************************************************
#this scripts iterates over the different language folders, subfolders and every file to
#obtain the number of words and number of articles per file

#usage: get_num_words_articles_wikipedia.sh [folder_with_all_files]
#Example Command: bash get_num_words_articles_wikipedia.sh extracted
#Example Results: metric.txt file with metrics for every file in a line
#           [language],[number_words],[number_articles]
#           e.g.   en,12345,321
#***************************************************
echo "======================================="
echo "Current time : $(date +"%T")"
    
if [ -f metrics.txt ]; then
    echo "Removing previous metrics.txt file"
    rm metrics.txt
fi
touch metrics.txt
num_files = 0
#Iterate over each extracted.[language]
for lang_folder in $1/* ; do
    echo "$lang_folder"
    re="(.*)\.([a-z]+)$"
    if [[ $lang_folder =~ $re ]]; then 
        lang=${BASH_REMATCH[2]};    
    fi

    #Iterate over every subfolder e.g. AA
    for hudrenth in $lang_folder/* ; do
        echo "$hudrenth"

        #Iterate over every file
        for file in $hudrenth/* ; do
            num_words=$(wc -w < $file)
            num_articles=$(grep -o "</doc>" $file | wc -l)
            echo "$lang,$num_words,$num_articles" >>metrics.txt
            ((num_files++))
        done
    done
done

echo "Done: I review $num_files files. Current time: $(date +"%T")"