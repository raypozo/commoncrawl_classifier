#!/bin/bash

for FILE in $(ls compressed) ; do
    LANGUAGE=$(python obtain_language_from_file.py $FILE 1)
    echo "Uncompressing compressed.bz2 file, $LANGUAGE language"
    if [ -d "decompressed/$LANGUAGE" ]; then
        continue
    fi
    bunzip2 -c -k "compressed/compressed.$LANGUAGE.bz2" > current.xml
    wikiextractor/WikiExtractor.py current.xml  -q -o "decompressed/$LANGUAGE"
    rm current.xml
done
