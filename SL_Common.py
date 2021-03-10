# SL_Common.py
# SetLineid common class

# Read from file, backup file, write file, find files by extension functionality

import os


class Common:
    def __init__(self):
        pass

    # Read text from file, each line as a list element
    @staticmethod
    def readFile(path):
        sData = []
        with open (path, "r") as fRead:
            lines = fRead.readlines()
        for line in lines:
            sData.append(line.strip())
        return sData

    # Backup files without overwriting existing ones (hording), if present
    @staticmethod
    def backupFile(path, backupPath):
        tryN = 1
        if backupPath == None or backupPath == "":
            backupPath = f"{path}.fc"
        while os.path.exists(backupPath):
            backupPath = f"{path}_{tryN}.fc"
            tryN += 1
        fRead = Common.readFile(path)
        Common.writeFile(fRead, backupPath)

    # Write data (text) to file line-by-line
    @staticmethod
    def writeFile(sData, path):
        with open (path, "w") as fWrite:
            for line in sData:
                fWrite.write(f"{line}\n")

    # Creates list of file pathes
    @staticmethod
    def filePathCollector(dirPath, fileExt):
        pathList = []
        for root, dirs, files in os.walk(dirPath):
            for f in files:
                if f.endswith(fileExt):
                    filePath = dirPath + f
                    pathList.append(filePath)

        return pathList
