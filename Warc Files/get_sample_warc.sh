
warc_commoncrawl_example=$1
touch sample.warc
head -n10000 warc_commoncrawl_example >> sample.warc
echo "END of sample file" >> sample.warc 

# touch sample_index.txt
# head -n1000 index_commoncrawl_example >> sample_index.txt
# echo "END of sample index file" >> sample_index.txt

