
import re 
  
# reading given tsv file 
with open("Genetics_Table.tsv", 'r') as myfile:   
  with open("Genetics_Table_v3.csv", 'w') as csv_file: 
    for line in myfile: 
        
      # Replace every tab with comma 
      fileContent = re.sub("\t", ",", line) 
        
      # Writing into csv file 
      csv_file.write(fileContent) 