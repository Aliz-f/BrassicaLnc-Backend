import csv

import json 
from models import chemicalFpk
from rest_framework import serializers, status

class chemicalSerializer(serializers.ModelSerializer):
    class Meta:
        model=chemicalFpk
        fields = "__all__"

def csv_to_json(csvFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
    #print(jsonArray[0])
    for i in jsonArray:
        ser = chemicalSerializer(data=i)
        if ser.is_valid():
            ser.save()
        else:
            print(i)
            print(ser.errors)
            break
csvFilePath = r'Chimical_fpkm.csv'

csv_to_json(csvFilePath, jsonFilePath)