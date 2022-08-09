# projeto_final_spark_semantix
Projeto final do bootcamp de engenheiro de bigdata


source : https://mobileapps.saude.gov.br/esus-vepi/files/unAFkcaNDeXajurGB7LChj8SgQYS2ptm/04bd3419b22b9cc5c6efac2c6528100d_HIST_PAINEL_COVIDBR_06jul2021.rar


1- copiar para dentro do docker

      #criar diretorio temp no container

      docker exec -it namenode mkdir /temp

      #criar diretorio temp no container

      docker exec -it namenode mkdir /temp/excel

      #copiar arquivos para diretorio dentro do container

      docker cp /home/ubuntu/Downloads/excel namenode:/temp

      #colocar dentro do hdfs

      docker exec -it namenode hdfs dfs -put /temp/excel  /user/jairomonassa/covid

      #verificar se os arquivos estao la

      docker exec -it namenode hdfs dfs -ls /user/jairomonassa/covid/excel


      #remover a pasta temporaria do container

      docker exec -it namenode rm -R /temp/excel
      
  2 - criar tabela do hive usando beeline
  
      docker cp /home/ubuntu/treinamentos/spark/covid.hsql hive-server:/opt
      
      docker exec -it hive-server beeline -u jdbc:hive2:// -n hive -p hive -f covid.hsql >> out.txt
      
      rodar a query covid.hsql
      
  3 - rodar o jobs para gravar no hive 
  
    * foi criado um notebook só para exploração e teste, mas será rodado pelo job
    
    ** curl -O https://repo1.maven.org/maven2/com/twitter/parquet-hadoop-bundle/1.6.0/parquet-hadoop-bundle-1.6.0.jar
    
    *** docker cp parquet-hadoop-bundle-1.6.0.jar jupyter-spark:/opt/spark/jars
    
    docker cp covid_excel.py jupyter-spark://bin
    
    docker exec -it jupyter-spark spark-submit --master yarn --deploy-mode client --queue root.bi.carga --executor-memory 12g --executor-cores 8 --total-executor-cores 8 /bin/covid_excel.py
    #ultimos dados do brasil
    df_brazil = df_covid.where(col("regiao")=='Brasil')\
               .orderBy(col("data").desc())\
               .limit(1)
               
    # pegar o ultimos recuperados e em acompanhamento
    df1 = df_brazil\
                 .select(col('recuperadosnovos'),col('emacompanhamentonovos'))\
                 .limit(1) 
    #df1.show()
    df1.write.mode("overwrite").parquet("/user/jairomonassa/v1")
    
    df2 = df_brazil\
               .select(col('casosnovos'),col('casosacumulado'))\
               .limit(1)
    #df2.show()  
    df2.write.mode("overwrite").parquet("/user/jairomonassa/v2")
    
    df3 = df_brazil\
                 .withColumn("letalidade",col("obitosacumulado")/col('casosacumulado')*100)\
                 .withColumn("letalidade",round(col("letalidade"),2))\
                 .withColumn("mortalidade",col("obitosacumulado")/col('populacaotcu2019'))\
                 .withColumn("mortalidade",round(col("mortalidade"),2))\
                 .select(col('obitosacumulado'),col('obitosnovos'),col("letalidade"),col("mortalidade"))\
                 .limit(1)
    #df3.show()
    df3.write.mode("overwrite").parquet("/user/jairomonassa/v3")


