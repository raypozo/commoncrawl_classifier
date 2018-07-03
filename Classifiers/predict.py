#import findspark
#findspark.init()
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql.types import StructType, StructField, DoubleType, StringType
from pyspark.sql.functions import rand
from pyspark.ml.feature import CountVectorizer, Tokenizer, StringIndexer
from pyspark.ml.feature import IndexToString
from pyspark.ml.classification import NaiveBayes, NaiveBayesModel
from pyspark.ml import Pipeline, PipelineModel
import re
import time


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


SparkContext.setSystemProperty('spark.executor.memory', '6g')
conf = SparkConf().setAppName("NBClassifier").setMaster("local[*]")
sc = SparkContext(conf=conf)
sc._jsc.hadoopConfiguration().set("textinputformat.record.delimiter", "</end_of_article>")
spark = SparkSession(sc)
sc.setLogLevel("ERROR")

model_nb = PipelineModel.read().load("model_nb_5k.save")
language_indexer = model_nb.stages[2].labels #Language list as in StringIndexer
print(language_indexer)

start = time.time()
schema = StructType([StructField("fullText", StringType(), True), StructField("lang", StringType(), False)])
#df = sc.textFile('example.txt')
df = sc.textFile('wet_concatenated.txt')
df = df.map(remove_syntax)
df = df.map(lambda l: (l, 'en')).toDF(schema)
print('Dataframe created')
p = model_nb.transform(df)
print('Prediction made..')
end = time.time()
print('Time to predict: {}'.format(end-start))
p_filter=p.select("prediction")
print(p.count())
i = 0
for p in p_filter.collect():
    print(i,p)
    i+=1
#print(p_filter.collect())
