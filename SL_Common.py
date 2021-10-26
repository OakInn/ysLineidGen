# SL_Common.py
# SetLineid common class

# """Functionality:
# - Read from file
# - Backup file
# - Write to file
# - Find files by extension recursively"""
# - WIP - Restore files from backup
# - Rules for lines to skip
# - Rules for line blocks to skip

import os


class Common:
    def __init__(self):
        pass

    # Read text from file, each line as a list element
    @staticmethod
    def readFile(path):
        sData = []
        with open (path, encoding="utf8") as fRead:
            lines = fRead.readlines()
        for line in lines:
            sData.append(line.strip("\n"))
        return sData

    # Backup files without overwriting existing ones (hording), if present
    @staticmethod
    def backupFile(path, backupPath):
        tryN = 1
        fileName = os.path.basename(path)
        if backupPath == None or backupPath == "":
            backupPath = f"{path}"
        else:
            backupPath = os.path.normpath(f"{backupPath}/{fileName}.fc")
        
        backupPathCopy = backupPath
        
        while os.path.exists(backupPath):
            if os.path.isdir(backupPath):
                backupPath = os.path.normpath(f"{backupPathCopy}/{fileName}_{tryN}.fc")
            elif os.path.isfile(backupPath):
                backupPath = os.path.normpath(f"{backupPathCopy}_{tryN}.fc")
                
            tryN += 1
        fRead = Common.readFile(path)
        Common.writeFile(fRead, backupPath)

    # Write data (text) to file line-by-line
    @staticmethod
    def writeFile(sData, path):
        with open (path, "w", encoding="utf8") as fWrite:
            for line in sData:
                fWrite.write(f"{line}\n")

    # Creates list of file pathes
    @staticmethod
    def filePathCollector(dirPath, fileExts):
        pathList = []
        for root, dirs, files in os.walk(dirPath):
            for f in files:
                # check if file with any needed extension found
                for ext in fileExts:
                    if f.endswith(ext):
                        # add file to list
                        filePath = os.path.join(root, f)
                        pathList.append(filePath)
                        break

        return pathList

    # Default/Simple/Basic line skip selector 
    @staticmethod
    def skipLinesDefaultSelector(line: str) -> bool:
        skipLine = False
        sLine = line.strip()

        # As Comment/Lore should be the last element, \
        # any LineTag there should be neglected.
        if sLine.startswith("//"):
            skipLine = True
        elif sLine.find("//") != -1:
            sLine = sLine.split("//", 1)[0].strip()

        if skipLine or not sLine or sLine.find("#line:skip") != -1 or sLine == "---" or sLine == "===":
            skipLine = True

        return skipLine


    # Text block skip selector 
    @staticmethod
    def skipBlockSelector(line: str, skipTrigger: bool, boxTrigger: bool) -> bool:
        sLine = line.strip()
        skip = Common.skipLinesDefaultSelector(line)
        vIdNeeded = False

        # <<box>> block
        if sLine.startswith("<<endbox>>"):
            boxTrigger = False
            skipTrigger = False
        elif sLine.startswith("<<box>>"):
            if sLine.startswith("<<box>>") and boxTrigger:
                pass
            else:
                boxTrigger = True
                skipTrigger = False

        # YarnSpinner node body block
        if not boxTrigger:
            if sLine.startswith("---"):
                vIdNeeded = True
                skipTrigger = False
            elif sLine.startswith("==="):
                skipTrigger = True
                vIdNeeded = False
            else:
                if not skipTrigger:
                    vIdNeeded = True
        else:
            if skip:
                skipTrigger = True
            else:
                vIdNeeded = True

        return (vIdNeeded, skipTrigger, boxTrigger)