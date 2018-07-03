**language_metrics.ipynb**
Visualization of different metrics (Recall, Confusion matrix, Accuracy, etc) of the results obtained from the Wikipedia stratified test set classification.

**get_num_words_articles_wikipedia.sh**
This scripts iterates over the different language folders, subfolders and every file to obtain the number of words and number of articles per file. Generates metrics.txt output file.

**metrics.txt**
File with extracted information per wiki_file, format: 
`language/number_words/number_articles`