import os
import json
import csv


class FileOperations:
    def parseFileName(arg1, arg2):
        return os.path.join(arg1, arg2)

    def initJsonFile(configFilePath):
        configFile = open(configFilePath)
        return json.load(configFile)

    def readCsvFile(filePath):
        dList = []
        with open(filePath) as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
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

    def writeWordToCsv(filePath, word):
        f = open(filePath, 'a')
        writer = csv.writer(f)
        data = ['0', word]
        writer.writerow(data)
        f.close

    def getDirs(dir_path):
        dirs = []
        for path in os.listdir(dir_path):
            dir = os.path.join(dir_path, path)
            dirs.append(dir)

        return dirs

    def getFiles(dir_path, fileType):
        files = []
        for file in os.listdir(dir_path):
            if file.endswith(fileType) or fileType == 'all':
                if os.path.isfile(os.path.join(dir_path, file)):
                    files.append(file)

        return files
