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
