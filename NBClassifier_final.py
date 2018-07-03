#Use example: python NBClassifier.py doc_num_threshold numchars_lower_bound test_ratio
import argparse
import numpy as np
import csv
import re
import time
import os,sys
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql.types import StructType, StructField, DoubleType, StringType
from pyspark.sql.functions import rand
from pyspark.ml.feature import CountVectorizer, Tokenizer, StringIndexer
from pyspark.ml.classification import NaiveBayes
from pyspark.ml import Pipeline

def create_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('--doc_num_threshold', type=int, default=100,
                      help='Number of documents per language')
  parser.add_argument('--numchars_lower_bound', type=int, default=100,
                      help='Minimum number of characters per article')
  parser.add_argument('--test_ratio', type=float, default=0.2,
                      help='Train to Test ratio')
  parser.add_argument('--num_cores', type=int, default=4,
                      help='Number of cores for spark configuration')
  return parser

# Spark Configuration function, defines master and assigns memory for excecution
def config_spark(num_cores):
    conf = SparkConf().setAppName("NB_Classifier")
    conf = conf.setMaster('yarn')\
    		 .set('spark.deploy-mode', 'cluster')\
             .set('spark.driver.memory', '6G')\
             .set('spark.driver.maxResultSize', '6G')
    sc = SparkContext(conf=conf)
    spark.rpc.message.maxSize=512
    sc.setLogLevel("ERROR")
    spark = SparkSession(sc)
    return spark

# Defines regex, Set for punctuation and doc open tag removal over RDDs
def remove_syntax(line):
    begin_re = re.compile("<doc [^>]*>")
    punct_re = re.compile(r'[^\w\s]', re.UNICODE)
    space_re = re.compile(' +')
    line = line.strip()
    line = begin_re.sub('', line)
    line = punct_re.sub('', line)
    line = space_re.sub('_', line)
    line=' '.join([line[i:i+3] for i in range(0, len(line), 3)])
    return line

# Auxiliary function to load articles per language and filter
def load_lang(lang_name,spark,schema,doc_num_threshold,lower_bound,rdm_seed):
    file_names = "decompressed/{}/AA/wiki_*".format(lang_name)
    sys.stdout.write('Loading language:'+lang_name +'\n')
    text_files = spark.sparkContext.newAPIHadoopFile(file_names, "org.apache.hadoop.mapreduce.lib.input.TextInputFormat",
            "org.apache.hadoop.io.LongWritable", "org.apache.hadoop.io.Text",
            conf={"textinputformat.record.delimiter": "</doc>\n"}).map(lambda l:l[1])

    ### Addition of filter to control minimum size(characters) per article:
    text_files_wfilter = text_files.filter(lambda x: len(x)>lower_bound)

    ### Sampling to get a fixed number of articles per language
    doc_num=text_files_wfilter.count()
    if doc_num>doc_num_threshold:
        convert_ratio=doc_num_threshold/float(doc_num)
        text_sampled=text_files_wfilter.sample(False, convert_ratio, rdm_seed)
        return text_sampled.map(remove_syntax).map(lambda l: (l, lang_name)).toDF(schema)
    # If not enough articles to filter, return all available articles
    else:
        return text_files_wfilter.map(remove_syntax).map(lambda l: (l, lang_name)).toDF(schema)

# Function to load, preprocess and filter data per number of articles and size per language
def sample_lang(spark,doc_num_threshold,numchars_lower_bound,test_ratio):
    exclusion_list = ["lawiki", 'aawiki', 'krwiki', 'hzwiki', '.DS_Store']
    #langs = [l for l in os.listdir("decompressed") if l not in exclusion_list]
    langs = ['en','ceb','sv','de','fr','nl','ru','it','es','pl','war','vi','ja','zh',
			 'pt','uk','sr','fa','ca','ar','no','sh','fi','hu','id','ko','cs','ro',
			 'ms','tr','eu','eo','bg','hy','da','sk','he','min','kk','hr','lt','et',
			 'ce','sl','be','gl','el','ur','nn','az','uz','la','hi','th','ka','vo','ta',
			 'cy','mk','tg','tl','mg','oc','lv','ky','tt','bs','ast','sq','new','azb',
			 'te','pms','br','bn','ml','jv','ht','lb','mr','sco','af','ga','pnb','is',
			 'ba','cv','sw','fy','su','my','lmo','an','yo','ne','nds','pa','gu','io','scn']
    schema = StructType([StructField("fullText", StringType(), True), StructField("lang", StringType(), False)])
    rdm_seed = 1234             #Random seed for sampling
    start = time.time()
    training_articles = spark.createDataFrame([], schema)
    testing_articles = spark.createDataFrame([], schema)
    # Loop over the language list and get the raw article text for each language
    for lang in langs:
        lang_training, lang_testing = load_lang(lang,spark,schema,doc_num_threshold,numchars_lower_bound,rdm_seed).randomSplit([1-test_ratio, test_ratio])
        sys.stdout.write('Number of training files: '+ str(lang_training.count())+'\tNumber of testing files: '+ str(lang_testing.count())+'\n')
        training_articles = training_articles.unionAll(lang_training)
        testing_articles = testing_articles.unionAll(lang_testing)

    training_articles = training_articles.orderBy(rand())
    testing_articles=testing_articles.orderBy(rand())
    print("{} languages loaded. {} training articles, {} testing articles".format(len(langs),training_articles.count(),testing_articles.count()))
    end =time.time()
    print("Time taken for loading:", end-start)
    return training_articles,testing_articles,langs

# Function to define the spark pipeline and train the model
def training(training_articles):
    tokenizer = Tokenizer(inputCol="fullText", outputCol="words")
    cv = CountVectorizer(inputCol="words", outputCol="wordsCountVector")
    si = StringIndexer(inputCol="lang", outputCol="langId")
    nb = NaiveBayes(featuresCol="wordsCountVector", labelCol="langId", modelType="multinomial")
    pipeline = Pipeline(stages=[tokenizer, cv, si, nb])
    start=time.time()
    model_nb = pipeline.fit(training_articles)
    end=time.time()
    print("Time taken to train:",end-start)
    return model_nb

def testing(model,testing_articles):
    # Run the classifier on the test sets
    start=time.time()
    tf = model_nb.transform(testing_articles)
    end=time.time()
    print("Time taken to test:",end-start)
    return tf


if __name__=='__main__':
    args = create_parser().parse_args()
    doc_num_threshold=args.doc_num_threshold
    numchars_lower_bound=args.numchars_lower_bound
    test_ratio=args.test_ratio
    num_cores=args.num_cores
    spark = config_spark(num_cores)
    training_articles,testing_articles,langs = sample_lang(spark,doc_num_threshold,numchars_lower_bound,test_ratio)
    model_nb=training(training_articles)
    model_nb.save("model_nb.save")
    tf = testing(model_nb,testing_articles)
    tf_filter=tf.select("lang","langId","prediction","probability")
    tf_filter.rdd.saveAsTextFile('output')
