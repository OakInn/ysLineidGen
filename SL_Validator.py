# SL_Validator.py
# SetLineid Validator class

# - Extract lineid if present
# - Validate lineid - hex-type and length (user choice - 3 or 8 bytes)
# - Validate whether there is a conflict (duplicate lineid)
# - Validate whether the line needs lineid


from SL_Extractor import Extractor

class Validator:
    def __init__(self):
        self.lineNAll = 0 # total amount of lines through all processed files
        self.lineNFile = 0 # counter of lines in currently processed file
        self.conflictN = 0 # total amount of conflicts through all processed files
        self.conflictDic = {} # dictionary of found conflicts
        self.lineidUsedDic = {} # dictionary of all unique lineids used in processed files
        self.idNeeded = False # general trigger which indicates if line needs lineid
        
    # Function which should be called for line validation.
    # Extract lineid, validate if it is hex number, validate lineid conflict
    def validatorProcess(self, filePath, sData):
        self.lineNFile = 0

        for sLine in sData:
            self.lineNFile += 1

            lineid = Extractor.extractLineid(sLine)

            if lineid == None or not lineid:
                continue
            hexValid = Validator.validateHexType(lineid)
            if hexValid:
                self.__validateConflict(lineid, filePath)

        self.lineNAll = self.lineNAll + self.lineNFile

    # Validate if conflict present and writes either into conflict dictionary
    # or into the dictionary of used unique lineids.
    def __validateConflict(self, lineid, filePath):
        if lineid in self.lineidUsedDic:
            self.addToConflictDic(f"{filePath}_Line{self.lineNFile}", f"conflict with {self.lineidUsedDic[lineid]}")
        else:
            self.addToLineidUsedDic(lineid, f"{filePath}_Line{self.lineNFile}")

    # Validate if lineid is a hex number
    @staticmethod
    def validateHexType(lineid):
        try:
            int(lineid, 16)
            return True
        except:
            return False
    # Setters
    # Add lineid to dictionary of used unique lineids
    def addToLineidUsedDic(self, key, value):
        self.lineidUsedDic[key] = str(value)

    # Add lineid to conflict dictionary
    def addToConflictDic(self, key, value):
        self.conflictDic[key] = str(value)
        self.conflictN += 1
    # Getters
    # Get conflict dictionary
    def getConflictDic(self):
        return self.conflictDic

    # Get dictionary of used lineids
    def getLineidUsedDic(self):
        return self.lineidUsedDic

    # Method which determine whether text line needs a lineid added.
    def validateLineidIsNeeded(self, line):
        """Method which determine whether text line needs a lineid added."""
        sLine = line.replace("##", "@NotComment@")

        if self.idNeeded == False:
            result = False
        else:
            if not sLine or sLine.startswith("#"):# empty line or fully commented
                result = False
            elif sLine.startswith("<<"):# command
                # go to ADDON!!! and decide do you need this line or not
                if not sLine.split(">>", 1)[1].strip():
                    result = False
                elif len(sLine.split(">>", 1)) > 1 and sLine.split(">>", 1)[1].strip()[0].isalnum() == False:
                    result = False
                else:
                    result = True
            elif sLine.startswith("[["):# choice options
                result = (sLine.find("|") != -1)
            else:
                result = True

        return result

    # Check lineid is of 3 or 8 byte long, or author's own decided length
    @staticmethod
    def validateHexLength(lineid):
        hexYarn = 6 # Representation of 3-byte length number
        hexLong = 16 # Representation of 8-byte length number
        lenYarn = "yarn" # Three byte long lineid
        lenLong = "long" # Eight byte long lineid
        lenOwn = "ownLen" # Author's own lineid length


        if len(lineid) == hexYarn:
            hexLen = lenYarn
        elif len(lineid) == hexLong:
            hexLen = lenLong
        else:
            hexLen = lenOwn

        return hexLen