# import time 
# import sys
# import requests
import os
filePath = os.getcwd() +'/files'

#*** Create LNC dataBase
# import requests
# import time 
# fasta_file = f"{filePath}/Final_lncRNA_rename_V2.fa"
# lnc_file = f"{filePath}/BrassicaLnc_Final_lncRAN_Table_Database.tsv"

# def parse_fasta(fname):
#     with open(fname, "r") as fh:
#         identifier = None
#         sequence = []

#         for line in fh:
#             line = line.strip() 
#             if line.startswith(">"):
#                 if identifier is None:
#                     identifier = line
#                 else:
#                     yield identifier, sequence
#                     identifier = line
#                     sequence = []
#             else:
#                 sequence.append(line)
# a= dict()
# for entry in parse_fasta(fasta_file):
#     chr = entry[0].split("|")[1].split(":")
#     a[entry[0].split("|")[0].strip(">")]={"data":"".join(entry[1]),"chr":chr[0],"location":chr[1]}

# ans = []

# with open(lnc_file) as f:
#   for line in f:
#     l=line.split('\t')
#     ans.append(l)

# key = ans[0]
# data=[]
# for i in ans[1:]:
#     d=dict()
#     try:
#         for j in range(len(key)):
#             d[key[j].strip("\n")]= i[j].strip()
#             d["sequence"] = a[i[0].strip()]["data"]
#         data.append(d)
#     except:
#         pass


# for i in range(len(data)):
#     data[i]["geneId"] = data[i].pop('Gene ID')
#     data[i]["transcriptId"] = data[i].pop('Transcript ID')
#     data[i]["stringTieId"] = data[i].pop('StringTie ID')
#     data[i]["chr"] = data[i].pop('Chr')
#     data[i]["location"] = data[i].pop('Location')
#     data[i]["length"] = data[i].pop('Length')
#     data[i]["exonNumber"] = data[i].pop('Exon number')
#     data[i]["classification"] = data[i].pop('Classification')

# # print(data[0])

# url = 'http://127.0.0.1:8000/lncRNA/set/'
# for i in range(len(data)):
#     response = requests.post(url, data=data[i])
#     print(response)
#     time.sleep(0.1)


#*** Create GTF dataBase
# import requests
# import time
# gtf_file = f"{filePath}/lncRNA.gtf"
# temp = []
# data = []
# each_data=dict()
# with open(gtf_file, 'r') as gtf:
#     for line in gtf:
#         line= line.strip("\n")
#         line = line.split('\t')
#         temp.append(line)
    
#     for value in temp:
#         each_data['chr'] = value[0]
#         each_data['stringTie'] = value[1]
#         each_data['exon'] = value[2]
#         each_data['locStart'] = value[3]
#         each_data['locEnd'] = value[4]
#         each_data['number'] = value[5]
#         each_data['symbol1'] = value[6]
#         each_data['symbol2'] = value[7]
#         template = value[8].split('"')
#         each_data['gene_id'] = template[1]
#         each_data['transcript_id'] = template[3]
#         each_data['exon_number'] = template[5]
#         data.append(each_data)
#         each_data = dict()
    
# url = 'http://127.0.0.1:8000/lncRNA/create/gtf/'
# for i in range(len(data)):
#     response = requests.post(url, data=data[i])
#     print(response)
#     # time.sleep(0.1)

#*** Create chemical headrs
# abioticFpkm_file = f"{filePath}/chemical/chemical_fpkm.txt"
# abioticHeadrs_file = f"{filePath}/chemical/chemical_headrs.txt"
# with open (abioticFpkm_file, 'r') as fh:
#     iter = 0
#     for line in fh.readlines():
#         if iter == 0:
#             line = line.split('\t')
#             with open(abioticHeadrs_file, 'w') as writer:
#                 for i in range(len(line)):
#                     if i ==0:
#                         writer.writelines(line[i]+'=models.CharField(max_length=70, null=False)'+'\n')
#                     else:
#                         writer.writelines(line[i]+'=models.FloatField()'+'\n')
#         iter+=1

#*** Create chemical dataBase
# import csv
# import requests
# chemical_file = f"{filePath}/chemical_fpkm.txt"
# jsonArray = []
# #read csv file
# with open(chemical_file, encoding='utf-8') as csvf: 
#     #load csv file data using csv library's dictionary reader
#     csvReader = csv.DictReader(csvf) 

#     #convert each csv row into python dict
#     for row in csvReader: 
#         #add this python dict to json array
#         jsonArray.append(row)
# #print(jsonArray[0])
# k=0
# url = 'http://188.121.122.34/lncRNA/create/chemicaldb/'
# for i in jsonArray:
#     response = requests.post(url, data=i)
#     print(response)
#     # time.sleep(0.1)


#*** Create abiotic headers and Create abiotic dataBase
# import requests

# abioticFpkm_file = f"{filePath}/abiotic/abiotic_fpkm.txt"
# abioticHeadrs_file = f"{filePath}/abiotic/abiotic_headrs.txt"

# dict = {}
# headers = []
# list = []
# total = []
# with open (abioticFpkm_file, 'r') as fh:
#     iter = 0
#     for line in fh.readlines():
#         if iter == 0:
#             line = line.split('\t')
#             with open(abioticHeadrs_file, 'w') as writer:
#                 for i in range(len(line)):
#                     if i ==0:
#                         writer.writelines(line[i]+'=models.CharField(max_length=70, null=False)'+'\n')
#                         headers.append(line[i])
#                     else:
#                         line[-1] = line[-1].strip('\n')
#                         writer.writelines(line[i]+'=models.FloatField()'+'\n')
#                         headers.append(line[i])
#         else:
#             break
#         iter+=1
#

# with open(abioticFpkm_file, 'r') as f:
#     for line in f.readlines():
#             temp=line.split('\t')
#             if len(temp)==1:
#                 list.append(temp[0].split(' '))
#             else:
#                 list.append(temp)

#     for i in range(1,len(list)):
#         for j in range(1, len(list[i])):
#             list[i][j] = float(list[i][j]) 

# for data in list:
#     dict['lncRNAs'] = data[0]
#     for i in range(1, len(data)):
#         dict[f'{headers[i]}'] = data[i]
#     total.append(dict)
#     dict = {}

# url = 'http://188.121.122.34/lncRNA/create/abioticdb/'
# for i in total:
#     response = requests.post(url, data=i)
#     print(response)
#     # time.sleep(0.1)

#*** Create genetics headers and Create genetics dataBase
# import requests

# geneticsFpkm_file = f"{filePath}/genetics/genetics_fpkm.txt"
# geneticsHeadrs_file = f"{filePath}/genetics/genetics_headrs.txt"

# dict = {}
# headers = []
# list = []
# total = []
# with open ('exp/files/genetics/genetics_fpkm.txt', 'r') as fh:
#     iter = 0
#     for line in fh.readlines():
#         if iter == 0:
#             line = line.split('\t')
#             with open('exp/files/genetics/headers.txt', 'w') as writer:
#                 for i in range(len(line)):
#                     if i ==0:
#                         writer.writelines(line[i]+'=models.CharField(max_length=70, null=False)'+'\n')
#                         headers.append(line[i])
#                     else:
#                         line[i] = line[i].strip('\n')
#                         writer.writelines(line[i]+'=models.FloatField()'+'\n')
#                         headers.append(line[i])
#         else:
#             break

#         iter+=1


# with open('exp/files/genetics/genetics_fpkm.txt', 'r') as f:
#     for line in f.readlines():
#             temp=line.split('\t')
#             if len(temp)==1:
#                 list.append(temp[0].split(' '))
#             else:
#                 list.append(temp)

#     for i in range(1,len(list)):
#         for j in range(1, len(list[i])):
#             list[i][j] = float(list[i][j]) 

# for data in list:
#     dict['lncRNAs'] = data[0]
#     for i in range(1, len(data)):
#         dict[f'{headers[i]}'] = data[i]
#     total.append(dict)
#     dict = {}

# print(total[1])
# k=0
# url = 'http://188.121.122.34/lncRNA/create/geneticsdb/'
# # url = 'http://127.0.0.1:8000/lncRNA/create/geneticsdb/'
# for i in range(1, len(total)):
#     response = requests.post(url, data=total[i])
#     print(response)
#     # time.sleep(0.1)
#     print(k)

#*** Create developmental headers and Create developmental dataBase
# import requests

# geneticsFpkm_file = f"{filePath}/developmental/developmental_fpkm.txt"
# geneticsHeadrs_file = f"{filePath}/developmental/developmental_headrs.txt"

# dict = {}
# headers = []
# list = []
# total = []
# with open (geneticsFpkm_file, 'r') as fh:
#     iter = 0
#     for line in fh.readlines():
#         if iter == 0:
#             line = line.split('\t')
#             with open(geneticsHeadrs_file, 'w') as writer:
#                 for i in range(len(line)):
#                     if i ==0:
#                         writer.writelines(line[i]+'=models.CharField(max_length=70, null=False)'+'\n')
#                         headers.append(line[i])
#                     else:
#                         line[i] = line[i].strip('\n')
#                         writer.writelines(line[i]+'=models.FloatField()'+'\n')
#                         headers.append(line[i])
#         else:
#             break

#         iter+=1


# with open(geneticsFpkm_file, 'r') as f:
#     for line in f.readlines():
#             temp=line.split('\t')
#             if len(temp)==1:
#                 list.append(temp[0].split(' '))
#             else:
#                 list.append(temp)

#     for i in range(1,len(list)):
#         for j in range(1, len(list[i])):
#             list[i][j] = float(list[i][j]) 

# for data in list:
#     dict['lncRNAs'] = data[0]
#     for i in range(1, len(data)):
#         dict[f'{headers[i]}'] = data[i]
#     total.append(dict)
#     dict = {}

# print(total[1])
# k=0
# url = 'http://188.121.122.34/lncRNA/create/geneticsdb/'
# # url = 'http://127.0.0.1:8000/lncRNA/create/geneticsdb/'
# for i in range(1, len(total)):
#     response = requests.post(url, data=total[i])
#     print(response)
#     # time.sleep(0.1)
#     print(k)
