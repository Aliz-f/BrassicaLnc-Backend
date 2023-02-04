"""
initial database with call command django
    None load data to database
    -c or create_files for create json files and load data to database
"""
import os
import sys
import json
import django
from django.core.management import call_command

sys.path.append("../brassicaLncWeb")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brassicaLncWeb.settings")
django.setup()


root = os.getcwd()

class InitialLncDatabase:
    """Initial Lnc database"""
    def __init__(self, create_files):
        self.create_files = create_files
        self.lnc()
        self.gtf()
        self.genetics_fpkm()
        self.chemical_fpkm()
        self.abiotic_fpkm()
        self.biotic_fpkm()
        self.developmental_fpkm()
        self.premi_rna()
        self.small_rna()
        self.etms()
        self.statistic()
        self.traget_downgenes()
        self.target_downgenes_description()
        self.traget_upgenes()
        self.target_upgenes_description()

    def parse_fasta(self, fname):
        """parse fasta file"""
        with open(fname, "r", encoding="utf-8") as file_handeler:
            identifier = None
            sequence = []
            for line in file_handeler:
                line = line.strip()
                if line.startswith(">"):
                    if identifier is None:
                        identifier = line
                    else:
                        yield identifier, sequence
                        identifier = line
                        sequence = []
                else:
                    sequence.append(line)

    def lnc(self):
        """load Lncs data"""
        if self.create_files:
            fasta_data= dict()
            for entry in self.parse_fasta(root+"/files/lncRNAs.fa"):
                char = entry[0].split("|")[1].split(":")
                fasta_data[entry[0].split("|")[0].strip(">")]= \
                    {
                        "data":"".join(entry[1]),"chr":char[0],"location":char[1]
                    }
            prepare_data = list()
            with open((root+"/files/lncRANs_Table.tsv"), encoding="utf8") as lnc_file:
                for line in lnc_file:
                    temp_line=line.split('\t')
                    prepare_data.append(temp_line)

                key = prepare_data[0]
                data=[]
                for i in prepare_data[1:]:
                    temp_data=dict()
                    try:
                        for j in range(len(key)):
                            temp_data[key[j].strip("\n")]= i[j].strip()
                            temp_data["fields"] = {}
                            temp_data["fields"]["sequence"] = fasta_data[i[0].strip()]["data"]
                        data.append(temp_data)
                    except:
                        pass
                for i in range(len(data)):
                    data[i]["model"]="lncRNA.lnc"
                    data[i]["pk"]=f"{i+1}"
                    data[i]["fields"]["geneId"] = data[i].pop('Gene ID')
                    data[i]["fields"]["transcriptId"] = data[i].pop('Transcript ID')
                    data[i]["fields"]["stringTieId"] = data[i].pop('StringTie ID')
                    data[i]["fields"]["chr"] = data[i].pop('Chr')
                    data[i]["fields"]["location"] = data[i].pop('Location')
                    data[i]["fields"]["length"] = data[i].pop('Length')
                    data[i]["fields"]["exonNumber"] = data[i].pop('Exon number')
                    data[i]["fields"]["classification"] = data[i].pop('Classification')
                    data[i]["fields"]['locStart'] = data[i]["fields"]['location'].split('-')[0]
                    data[i]["fields"]['locEnd'] = data[i]["fields"]['location'].split('-')[1]
                with open("lnc.json", "w", encoding="utf-8") as lnc_json:
                    json.dump(data, lnc_json, indent=4)
                    print("Lnc file created!...")
                call_command("loaddata", "lnc.json")
        else:
            call_command("loaddata", "lnc.json")

    def gtf(self):
        """load Gtfs data"""
        if self.create_files:
            temp = []
            data = []
            each_data=dict()
            with open(root+"/files/lncRNAs.gtf", 'r', encoding="utf-8") as gtf:
                for line in gtf:
                    line= line.strip("\n")
                    line = line.split('\t')
                    temp.append(line)

                iterator = 1
                for value in temp:
                    each_data['model'] = "lncRNA.gtf"
                    each_data['pk'] = f"{iterator}"
                    each_data['fields'] = {}
                    each_data['fields']['chromosome'] = value[0]
                    each_data['fields']['stringTie'] = value[1]
                    each_data['fields']['exon'] = value[2]
                    each_data['fields']['locStart'] = value[3]
                    each_data['fields']['locEnd'] = value[4]
                    each_data['fields']['number'] = value[5]
                    each_data['fields']['strand1'] = value[6]
                    each_data['fields']['strand2'] = value[7]
                    template = value[8].split('"')
                    each_data['fields']['gene_id'] = template[1]
                    each_data['fields']['transcript_id'] = template[3]
                    each_data['fields']['exon_number'] = template[5]
                    data.append(each_data)
                    each_data = dict()
                    iterator +=1
                with open("gtf.json", "w", encoding="utf-8") as lnc_json:
                    json.dump(data, lnc_json, indent=4)
                    print("Gtf file created!...")

                call_command("loaddata", "gtf.json")
        else:
            call_command("loaddata", "gtf.json")

    def genetics_fpkm(self):
        """load genetics fpkm data"""
        if self.create_files:
            temp_dict = {}
            headers = []
            temp_list = []
            total = []
            with open (root+'/files/genetics/v2/genetics_fpkm.txt', 'r',
                encoding='utf-8') as file_handeler:
                iterator = 0
                for line in file_handeler.readlines():
                    if iterator == 0:
                        line = line.split('\t')
                        for i in range(len(line)):
                            if i ==0:
                                headers.append(line[i].replace("\n", ""))
                            else:
                                # line[i] = line[i].strip('\n')
                                headers.append(line[i].replace("\n", ""))
                    else:
                        break
                    iterator+=1

            with open(root+'/files/genetics/v2/genetics_fpkm.txt', 'r',
                encoding='utf-8') as file_handeler:
                for line in file_handeler.readlines():
                    temp=line.split('\t')
                    if len(temp)==1:
                        temp_list.append(temp[0].split(' '))
                    else:
                        temp_list.append(temp)

                for i in range(1,len(temp_list)):
                    for j in range(1, len(temp_list[i])):
                        temp_list[i][j] = float(temp_list[i][j])

            iterator = 0
            for data in temp_list:
                temp_dict['model'] = "lncRNA.geneticsfpkm"
                temp_dict['pk'] = f"{iterator}"
                temp_dict['fields'] = {}
                temp_dict['fields']['lncRNAs'] = data[0]
                for i in range(1, len(data)):
                    temp_dict['fields'][f'{headers[i]}'] = data[i]
                total.append(temp_dict)
                temp_dict = {}
                iterator +=1
            with open("genetics_fpkm.json", "w", encoding="utf-8") as lnc_json:
                json.dump(total[1:], lnc_json, indent=4)
                print("Genetics Fpkm file created!...")
            call_command("loaddata", "genetics_fpkm.json")
        else:
            call_command("loaddata", "genetics_fpkm.json")

    def chemical_fpkm(self):
        """load chemical fpkm data"""
        if self.create_files:
            temp_dict = {}
            headers = []
            temp_list = []
            total = []
            with open (root+'/files/chemical/v2/chemical_fpkm.txt', 'r',
                encoding='utf-8') as file_handeler:
                iterator = 0
                for line in file_handeler.readlines():
                    if iterator == 0:
                        line = line.split('\t')
                        for i in range(len(line)):
                            if i ==0:
                                headers.append(line[i].replace("\n", ""))
                            else:
                                # line[i] = line[i].strip('\n')
                                headers.append(line[i].replace("\n", ""))
                    else:
                        break
                    iterator+=1
            with open (root+'/files/chemical/v2/chemical_fpkm.txt', 'r',
                encoding='utf-8') as file_handeler:
                for line in file_handeler.readlines():
                    temp=line.split('\t')
                    if len(temp)==1:
                        temp_list.append(temp[0].split(' '))
                    else:
                        temp_list.append(temp)

                for i in range(1,len(temp_list)):
                    for j in range(1, len(temp_list[i])):
                        temp_list[i][j] = float(temp_list[i][j])

            iterator = 0
            for data in temp_list:
                temp_dict['model'] = "lncRNA.chemicalfpkm"
                temp_dict['pk'] = f"{iterator}"
                temp_dict['fields'] = {}
                temp_dict['fields']['lncRNAs'] = data[0]
                for i in range(1, len(data)):
                    temp_dict['fields'][f'{headers[i]}'] = data[i]
                total.append(temp_dict)
                temp_dict = {}
                iterator +=1
            with open("chemical_fpkm.json", "w", encoding="utf-8") as lnc_json:
                json.dump(total[1:], lnc_json, indent=4)
                print("Chemical Fpkm file created!...")
            call_command("loaddata", "chemical_fpkm.json")
        else:
            call_command("loaddata", "chemical_fpkm.json")

    def abiotic_fpkm(self):
        """load abiotic fpkm data"""
        if self.create_files:
            temp_dict = {}
            headers = []
            temp_list = []
            total = []
            with open (root+'/files/abiotic/v2/abiotic_fpkm.txt', 'r',
                encoding='utf-8') as file_handeler:
                iterator = 0
                for line in file_handeler.readlines():
                    if iterator == 0:
                        line = line.split('\t')
                        for i in range(len(line)):
                            if i ==0:
                                headers.append(line[i].replace("\n", ""))
                            else:
                                # line[i] = line[i].strip('\n')
                                headers.append(line[i].replace("\n", ""))
                    else:
                        break
                    iterator+=1
            with open (root+'/files/abiotic/v2/abiotic_fpkm.txt', 'r',
                encoding='utf-8') as file_handeler:
                for line in file_handeler.readlines():
                    temp=line.split('\t')
                    if len(temp)==1:
                        temp_list.append(temp[0].split(' '))
                    else:
                        temp_list.append(temp)

                for i in range(1,len(temp_list)):
                    for j in range(1, len(temp_list[i])):
                        temp_list[i][j] = float(temp_list[i][j])

            iterator = 0
            for data in temp_list:
                temp_dict['model'] = "lncRNA.abioticfpkm"
                temp_dict['pk'] = f"{iterator}"
                temp_dict['fields'] = {}
                temp_dict['fields']['lncRNAs'] = data[0]
                for i in range(1, len(data)):
                    temp_dict['fields'][f'{headers[i]}'] = data[i]
                total.append(temp_dict)
                temp_dict = {}
                iterator +=1
            with open("abiotic_fpkm.json", "w", encoding="utf-8") as lnc_json:
                json.dump(total[1:], lnc_json, indent=4)
                print("Abiotic Fpkm file created!...")
            call_command("loaddata", "abiotic_fpkm.json")
        else:
            call_command("loaddata", "abiotic_fpkm.json")

    def biotic_fpkm(self):
        """load biotic fpkm data"""
        if self.create_files:
            temp_dict = {}
            headers = []
            temp_list = []
            total = []
            with open (root+'/files/biotic/v2/biotic_fpkm.txt', 'r',
                encoding='utf-8') as file_handeler:
                iterator = 0
                for line in file_handeler.readlines():
                    if iterator == 0:
                        line = line.split('\t')
                        for i in range(len(line)):
                            if i ==0:
                                headers.append(line[i].replace("\n", ""))
                            else:
                                # line[i] = line[i].strip('\n')
                                headers.append(line[i].replace("\n", ""))
                    else:
                        break
                    iterator+=1
            with open (root+'/files/biotic/v2/biotic_fpkm.txt', 'r',
                encoding='utf-8') as file_handeler:
                for line in file_handeler.readlines():
                    temp=line.split('\t')
                    if len(temp)==1:
                        temp_list.append(temp[0].split(' '))
                    else:
                        temp_list.append(temp)

                for i in range(1,len(temp_list)):
                    for j in range(1, len(temp_list[i])):
                        temp_list[i][j] = float(temp_list[i][j])

            iterator = 0
            for data in temp_list:
                temp_dict['model'] = "lncRNA.bioticfpkm"
                temp_dict['pk'] = f"{iterator}"
                temp_dict['fields'] = {}
                temp_dict['fields']['lncRNAs'] = data[0]
                for i in range(1, len(data)):
                    temp_dict['fields'][f'{headers[i]}'] = data[i]
                total.append(temp_dict)
                temp_dict = {}
                iterator +=1
            with open("biotic_fpkm.json", "w", encoding="utf-8") as lnc_json:
                json.dump(total[1:], lnc_json, indent=4)
                print("Biotic Fpkm file created!...")
            call_command("loaddata", "biotic_fpkm.json")
        else:
            call_command("loaddata", "biotic_fpkm.json")

    def developmental_fpkm(self):
        """load developmental fpkm data"""
        if self.create_files:
            temp_dict = {}
            headers = []
            temp_list = []
            total = []
            with open (root+'/files/developmental/v2/developmental_fpkm.txt', 'r',
                encoding='utf-8') as file_handeler:
                iterator = 0
                for line in file_handeler.readlines():
                    if iterator == 0:
                        line = line.split('\t')
                        for i in range(len(line)):
                            if i ==0:
                                headers.append(line[i].replace("\n", ""))
                            else:
                                # line[i] = line[i].strip('\n')
                                headers.append(line[i].replace("\n", ""))
                    else:
                        break
                    iterator+=1
            with open (root+'/files/developmental/v2/developmental_fpkm.txt', 'r',
                encoding='utf-8') as file_handeler:
                for line in file_handeler.readlines():
                    temp=line.split('\t')
                    if len(temp)==1:
                        temp_list.append(temp[0].split(' '))
                    else:
                        temp_list.append(temp)

                for i in range(1,len(temp_list)):
                    for j in range(1, len(temp_list[i])):
                        temp_list[i][j] = float(temp_list[i][j])

            iterator = 0
            for data in temp_list:
                temp_dict['model'] = "lncRNA.developmentalfpkm"
                temp_dict['pk'] = f"{iterator}"
                temp_dict['fields'] = {}
                temp_dict['fields']['lncRNAs'] = data[0]
                for i in range(1, len(data)):
                    temp_dict['fields'][f'{headers[i]}'] = data[i]
                total.append(temp_dict)
                temp_dict = {}
                iterator +=1
            with open("developmental_fpkm.json", "w", encoding="utf-8") as lnc_json:
                json.dump(total[1:], lnc_json, indent=4)
                print("Developmental Fpkm file created!...")
            call_command("loaddata", "developmental_fpkm.json")
        else:
            call_command("loaddata", "developmental_fpkm.json")

    def premi_rna(self):
        """load PremiRna data"""
        if self.create_files:
            premirna_list = list()
            iterator = 0
            with open(root +
                '/files/multi_omics/premiRNA/BrassicaLnc_V2 - PremiRNA.tsv', 'r',
                encoding='utf-8') as file_handeler:
                for line in file_handeler.readlines():
                    temp = line.split('\t')
                    if iterator == 0:
                        pass
                    else:
                        premirna_list.append(temp)
                    iterator+=1
            data = list()
            iterator = 1
            for each in premirna_list:
                data.append(
                    dict(
                        model = "lncRNA.premirna",
                        pk = iterator,
                        fields = dict(
                        lncrna_id = each[0],
                        premi_rna = each[1],
                        identity= each[2],
                        alignment_length = each[3],
                        mismatches = each[4],
                        lncrna_start = each[5],
                        lncrna_end = each[6],
                        premi_rna_start = each[7],
                        premi_rna_end = each[8],
                        e_value = each[9],
                        bitscore = each[10],
                        structure = True if "TRUE" in each[11] else False,
                        )
                    )
                )
                iterator += 1
            with open("premirna.json", "w", encoding="utf-8") as lnc_json:
                json.dump(data, lnc_json, indent=4)
                print("Premi Rna file created!...")
            call_command("loaddata", "premirna.json")
        else:
            call_command("loaddata", "premirna.json")

    def small_rna(self):
        """load SmallRna data"""
        if self.create_files:
            smallrna_list = list()
            iterator = 0
            with open(root +
                '/files/multi_omics/smallRNA/BrassicaLnc_V2 - SmallRNATargets.tsv',
                 'r', encoding="utf-8") as file_handeler:
                for line in file_handeler.readlines():
                    temp = line.split('\t')
                    if iterator == 0:
                        pass
                    else:
                        smallrna_list.append(temp)
                    iterator+=1

            data = list()
            iterator = 1
            for each in smallrna_list:
                data.append(
                    dict(
                        model = "lncRNA.smallrnatarget",
                        pk = iterator,
                        fields = dict(
                            lncrna_id = each[0],
                            mirna_id = each[1],
                            expectation= each[2],
                            lncrna_start = each[3],
                            lncrna_end = each[4],
                            mirna_start = each[5],
                            mirna_end = each[6],
                            inhibition = each[7],
                            lncrna_aligned_fragment = each[8],
                            mirna_aligned_fragment = each[9],
                        )
                    )
                )
                iterator +=1
            with open("smallrna.json", "w", encoding="utf-8") as lnc_json:
                json.dump(data, lnc_json, indent=4)
                print("Small Rna file created!...")
            call_command("loaddata", "smallrna.json")
        else:
            call_command("loaddata", "smallrna.json")

    def etms(self):
        """"load etms data"""
        if self.create_files:
            etms_list = list()
            iterator = 0
            with open(root +
                '/files/multi_omics/etms/BrassicaLnc_V2 - eTMs.tsv',
                'r', encoding="utf-8") as file_handeler:
                for line in file_handeler.readlines():
                    temp = line.split('\t')
                    if iterator == 0:
                        pass
                    else:
                        etms_list.append(temp)
                    iterator+=1

            data = list()
            iterator = 1
            for each in etms_list:
                data.append(
                    dict(
                        model = "lncRNA.etms",
                        pk = iterator,
                        fields = dict(
                            lncrna_id = each[0],
                            mirna_id = each[1],
                            score= each[2],
                            lncrna_start = each[3],
                            lncrna_end = each[4],
                            mirna_start = each[5],
                            mirna_end = each[6],
                            alignment = each[7],
                            lnc_alignment = each[8],
                            mirna_alignment = each[9],
                        )
                    )
                )
                iterator+=1
            with open("etms.json", "w", encoding="utf-8") as lnc_json:
                json.dump(data, lnc_json, indent=4)
                print("Etms file created!...")
            call_command("loaddata", "etms.json")
        else:
            call_command("loaddata", "etms.json")

    def statistic(self):
        """load statistic data"""
        if self.create_files:
            filteration = dict(
                model = "statistic.filtrationstepslncrnaidentificationpipeline",
                pk = "1",
                fields = dict(
                    name = "The results of filtration steps in the lncRNA identification pipeline. Numbers represent the total number of transcripts filtered out in each step.",
                    data = {"Potential novel transripts (Class codes: i, u, x, o, e)": 31777, "Transcripts with length > 200 bp and < 15 kb": 30905, "Transcripts with FPKM > 0.5 in at least 495 samples": 5990, "Transcripts after filter out tRNAs and rRNAs": 5947, "Noncoding transcripts predicted by CPC2": 4766, "LncRNAs predicted by PLncPRO, FEElnc, and CREMA": 2321, "Transcripts with no significant hit against UniProt, Pfam, and Rfam.": 1852, "Reliably expressed lncRNAs": 1852}
                )
            )
            filteration_list = list()
            filteration_list.append(filteration)

            with open("filteration.json", "w", encoding="utf-8") as lnc_json:
                json.dump(filteration_list, lnc_json, indent=4)
                print("Filteration file created!...")
            call_command("loaddata", "filteration.json")
            relationship = dict(
                model = "statistic.relationshipbetweenchrgenelncrna",
                pk = "1",
                fields = dict(
                    name = 'The quantitative relationship between Chromosome, Gene and LncRNA',
                    data = {"chromosome": 41, "mRNA": 101040, "lncRNA": 1856}
                )
            )
            relationship_list=list()
            relationship_list.append(relationship)

            with open("relationship.json", "w", encoding="utf-8") as lnc_json:
                json.dump(relationship_list, lnc_json, indent=4)
                print("Relationship file created!...")
            call_command("loaddata", "relationship.json")
            subdivision = dict(
                model = "statistic.subdivisionlncrnasaccordingclasscodes",
                pk = "1",
                fields = dict(
                    name = "Subdivision of lncRNAs according to the class codes (“u,” “x,” “i,” “o,” and “e”)",
                    data ={"intronic lncRNAs (i)": 25, "generic exonic overlap lncRNAs with reference transcripts (o)": 178, "intergenic lncRNAs (u)": 1645, "antisense lncRNAs (x)": 0}
                )
            )
            subdivision_list = list()
            subdivision_list.append(subdivision)
            with open("subdivision.json", "w", encoding="utf-8") as lnc_json:
                json.dump(subdivision_list, lnc_json, indent=4)
                print("Subdivision file created!...")
            call_command("loaddata", "subdivision.json")
        else:
            call_command("loaddata", "filteration.json")
            call_command("loaddata", "relationship.json")
            call_command("loaddata", "subdivision.json")

    def traget_downgenes(self):
        """load target downgene data"""
        if self.create_files:
            target_lines = list()
            data = list()
            with open(root + "/files/multi_omics/target/down_genes/LncTar_Downgenes.txt",
            "r", encoding="utf-8") as file_handeler:
                for line in file_handeler.readlines():
                    temp_line = line.split("\t")
                    temp_line = [each.strip() for each in temp_line]
                    target_lines.append(temp_line)
                del target_lines[0]
                iterator = 1
                for each in target_lines:
                    data.append(
                        dict(
                            model = "lncRNA.targetdowngene",
                            pk = f"{iterator}",
                            fields = dict(
                                query = each[0],
                                length_query = each[1],
                                target = each[2],
                                length_target = each[3],
                                dg = each[4],
                                ndg = each[5],
                                start_position_query = each[6],
                                end_position_query = each[7],
                                start_position_target = each[8],
                                end_position_target = each[9],
                            )
                        )
                    )
                    iterator += 1
            with open("target_downgene.json", "w", encoding="utf-8") as lnc_json:
                json.dump(data, lnc_json, indent=4)
                print("Target Downgenes file created!...")
            call_command("loaddata", "target_downgene.json")
        else:
            call_command("loaddata", "target_downgene.json")

    def target_downgenes_description(self):
        """load target downgenes description data"""
        if self.create_files:
            description_lines = list()
            data = list()
            with open(root + "/files/multi_omics/target/down_genes/Downgenes_description.txt",
            "r", encoding="utf-8") as file_handeler:
                for line in file_handeler.readlines():
                    temp_line = line.split('\t')
                    temp_line = [each.strip() for each in temp_line]
                    description_lines.append(temp_line)
                del description_lines[0]

                iterator = 1
                for each in description_lines:
                    data.append(
                        dict(
                            model = "lncRNA.downgenedescription",
                            pk = f"{iterator}",
                            fields = dict(
                                gene_id = each[0],
                                chromosome = each[1],
                                start = each[2],
                                stop = each[3],
                                strand = each[4],
                                description = each[5],
                            )
                        )
                    )
                    iterator += 1
            with open("target_downgenes_description.json", "w", encoding="utf-8") as lnc_json:
                json.dump(data, lnc_json, indent=4)
                print("Target Downgenes Description file created!...")
            call_command("loaddata", "target_downgenes_description.json")
        else:
            call_command("loaddata", "target_downgenes_description.json")

    def traget_upgenes(self):
            """load target downgene data"""
            if self.create_files:
                target_lines = list()
                data = list()
                with open(root + "/files/multi_omics/target/up_genes/LncTar_Upgenes.txt",
                "r", encoding="utf-8") as file_handeler:
                    for line in file_handeler.readlines():
                        temp_line = line.split("\t")
                        temp_line = [each.strip() for each in temp_line]
                        target_lines.append(temp_line)
                    del target_lines[0]
                    iterator = 1
                    for each in target_lines:
                        data.append(
                            dict(
                                model = "lncRNA.targetupgene",
                                pk = f"{iterator}",
                                fields = dict(
                                    query = each[0],
                                    length_query = each[1],
                                    target = each[2],
                                    length_target = each[3],
                                    dg = each[4],
                                    ndg = each[5],
                                    start_position_query = each[6],
                                    end_position_query = each[7],
                                    start_position_target = each[8],
                                    end_position_target = each[9],
                                )
                            )
                        )
                        iterator += 1
                with open("target_upgene.json", "w", encoding="utf-8") as lnc_json:
                    json.dump(data, lnc_json, indent=4)
                    print("Target Upgenes file created!...")
                call_command("loaddata", "target_upgene.json")
            else:
                call_command("loaddata", "target_upgene.json")

    def target_upgenes_description(self):
        """load target downgenes description data"""
        if self.create_files:
            description_lines = list()
            data = list()
            with open(root + "/files/multi_omics/target/up_genes/Upgenes_description.txt",
            "r", encoding="utf-8") as file_handeler:
                for line in file_handeler.readlines():
                    temp_line = line.split('\t')
                    temp_line = [each.strip() for each in temp_line]
                    description_lines.append(temp_line)
                del description_lines[0]

                iterator = 1
                for each in description_lines:
                    data.append(
                        dict(
                            model = "lncRNA.upgenedescription",
                            pk = f"{iterator}",
                            fields = dict(
                                gene_id = each[0],
                                chromosome = each[1],
                                start = each[2],
                                stop = each[3],
                                strand = each[4],
                                description = each[5],
                            )
                        )
                    )
                    iterator += 1
            with open("target_upgenes_description.json", "w", encoding="utf-8") as lnc_json:
                json.dump(data, lnc_json, indent=4)
                print("Target Downgenes Description file created!...")
            call_command("loaddata", "target_upgenes_description.json")
        else:
            call_command("loaddata", "target_upgenes_description.json")

if __name__ == "__main__":
    create_command = bool("-c" in sys.argv or "create_files" in sys.argv)
    init_data = InitialLncDatabase(create_command)
