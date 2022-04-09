import pandas as pd
import sqlite3
import mysql.connector as mysql
from mysql.connector import Error
import mysql.connector as mysql
from mysql.connector import Error
a= "yMUvnDY6qW8B"

tsv_file='./Tabledb - Chemical_db.tsv'
# readinag given tsv file 
csv_table=pd.read_table(tsv_file,sep='\t') 
  
# converting tsv file into csv 
csv_table.to_csv('Tabledb - Chemical_db.csv',index=False) 

data= []
with open("Tabledb - Chemical_db.csv", 'r') as myfile:
    for line in myfile:
        data.append(line.split(","))
           

#print(len(data[0]))
#print(data[4])
#print(1)
dic=dict()
with open("bra  ", 'w') as myfile:
    for i in data:
        try:
            a=dic[i[4].split()[0]]
            a.append("".join(i[3].split())+"_"+i[2].split()[0])
            dic[i[4].split()[0]] = a
        except:
            dic[i[4].split()[0]]=  ["".join(i[3].split())+"_"+i[2].split()[0]]
            
    print(dic)
    for i in dic.keys():
        print(i)
        myfile.write(i + "="+'models.JsonField(default={"item": ' +str(dic[i])+"})"+"\n")