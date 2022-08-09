#!/usr/bin/env python
# coding, utf-8

import sys
import json
import pyspark.sql.functions as f
from pyspark.sql.functions import when, col
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, DateType, TimestampType, DecimalType
from pyspark import SparkContext, SparkConf, SQLContext, HiveContext
from collections import namedtuple
conf = (SparkConf().setAppName("covid"))
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
sql_ctx = SQLContext(sc)
spark = SparkSession(sc)


schema = StructType([ \
    StructField("regiao",StringType(),True), \
    StructField("estado",StringType(),True), \
    StructField("municipio",StringType(),True), \
    StructField("coduf", IntegerType(), True), \
    StructField("codmun", IntegerType(), True), \
    StructField("codRegiaoSaude", IntegerType(), True), \
    StructField("nomeRegiaoSaude",StringType(),True), \
    StructField("data",TimestampType(),True), \
    StructField("semanaEpi",IntegerType(),True), \
    StructField("populacaoTCU2019", IntegerType(), True), \
    StructField("casosAcumulado", DecimalType(), True), \
    StructField("casosNovos", IntegerType(), True) ,\
    StructField("obitosAcumulado", IntegerType(), True), \
    StructField("obitosNovos", IntegerType(), True), \
    StructField("Recuperadosnovos", IntegerType(), True), \
    StructField("emAcompanhamentoNovos", IntegerType(), True), \
    StructField("interior/metropolitana", IntegerType(), True), \
  ])

df = spark.read.option("header","true")\
 .option("schema",schema)\
 .option("mode","DROPMALFORMED")\
 .option("delimiter", ";")\
 .option("inferSchema", "true")\
 .csv("/user/jairomonassa/covid/excel/*.csv")


df= df.withColumnRenamed("codRegiaoSaude","codregiaosaude")\
	.withColumnRenamed("nomeRegiaoSaude","nomeregiaosaude")\
	.withColumnRenamed("semanaEpi","semanaepi")\
	.withColumnRenamed("populacaoTCU2019","populacaotcu2019")\
	.withColumnRenamed("casosAcumulado","casosacumulado")\
	.withColumnRenamed("casosNovos","casosnovos")\
	.withColumnRenamed("obitosAcumulado","obitosacumulado")\
	.withColumnRenamed("obitosNovos","obitosnovos")\
	.withColumnRenamed("emAcompanhamentoNovos","emacompanhamentonovos")\
	.withColumnRenamed("interior/metropolitana","interiormetropolitana")

df.write.mode("overwrite").partitionBy("municipio").saveAsTable("covid")

