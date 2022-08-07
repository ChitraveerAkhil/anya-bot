import os
import json
import csv

class FileOperations:
    def parseFileName(arg1, arg2):
        return os.path.join(arg1,arg2)

    def initJsonFile(configFilePath):
        configFile = open(configFilePath)
        return json.load(configFile)

    def readCsvFile(filePath):
        dList = []
        with open(filePath) as csvFile:
            csvReader = csv.reader(csvFile,delimiter=',')
            dList = list(csvReader)

        count = 0
        rtnLst = []
        for row in dList:
            if count > 0:
                if row:
                    if row[1]:
                        rtnLst.append(row[1])
            count += 1
        return rtnLst

    def writeWordToCsv(filePath,word):
        f = open(filePath,'a')
        writer = csv.writer(f)
        data = ['0',word]
        writer.writerow(data)
        f.close
