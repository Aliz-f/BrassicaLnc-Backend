# import time 
# import sys
# import requests


# fasta_file = "./Final_lncRNA_rename_V2.fa"

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

# with open("./BrassicaLnc _Final_lncRAN_Table_Database.tsv") as f:
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
