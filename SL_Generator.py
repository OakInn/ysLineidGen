# SL_Generator.py
# Setline Generator class
# pip install libscrc 1.3 - for CRC generation.
# Generate new lineid in CRC24 or CRC64 hex format, or decide whether to skip line.

# Generation of new lineids is based on whether:
#   - line contains any text that needs to be translated to another language, \
# and currently does not have assigned valid and unique lineid
#   - line contains the request for lineid -> empty lineid tags in the end of the line- "#line:"
#   - lineid used in the lines conflicts with previously used one
#   - lineid is not a valid hex number
#   - lineid is valid hex number, but its length does not comply with user/default \
# compatibility settings.
# example -> if we have "...#line:250d" (here lineid length is 4 characters,
# or 2 bytes), but the setting is that all lineids should be of the yarn
# spinner length (which is 6 characters, or 3 bytes)
# Two methods - to incert and replace genarated lineid.

import sys

import libscrc
from SL_Extractor import Extractor
from SL_Common import Common


class Generator:
    def __init__(self, userChoice):
        self.common = Common()
        self.extract = Extractor()
        # Need two user choices - what lineid length (3/8 byte) should be.
        # For both newly created (newcompat) and those already present (compat)
        self.compat = userChoice["compat"]
        self.newcompat = userChoice["newcompat"]

        # User choice, which desides whether to resolve conflicts (duplicate lineid)
        self.resolve = userChoice["resolve"]
        # and in which way (generate new lineid with chosen length - 3/8 bytes).
        # These two are constants
        self.lenYarn = "yarn"# 3 bytes long lineid
        self.lenLong = "long"# 8 bytes long lineid
        
        # Variables for controlling persistant behavior.
            # Default. Skip all lines except those in Node body (lines between "---" and "===").
        self.skipTrigger = True
            # Special. Rules to skip lines in "box" (lines between "box" and "endbox").
        self.boxTrigger = False

    # Function which should be called for lineid generation
    def generatorProcess(self, filePath, sData, validator):
        lineN = 0# Line counter

        for line in sData:
            #Handle in-text double colon (::)
            if line.find("::") != -1:
                line = line.replace("::", "@quad@")

            lineN += 1

            validator.idNeeded, self.skipTrigger, self.boxTrigger = \
                self.common.skipBlockSelector(line, self.skipTrigger, self.boxTrigger)
            if self.skipTrigger:
                skipLine = True
            else:
                skipLine = False

            skipLine = self.common.skipLinesDefaultSelector(line)

            if skipLine:
                continue
            else:
                # Decide between skipping or generating lineid for a line
                line, skipLine = self.__lineFilter(filePath, lineN, line, validator)
                if skipLine:
                    continue

            #Handle in-text double colon (::). Reverting changes to original state.
            if line.find("@quad@") != -1:
                line = line.replace("@quad@", "::")

            sData[lineN-1] = line

        return sData

    # Skip or process lines in yarn file
    def __lineFilter(self, filePath, lineN, line, validator):
        lineid = self.extract.extractLineid(line)

        if not lineid:
            line, skip = self.__lineidAbsent(filePath, lineN, line, validator)

        else:
            line, skip = self.__lineidPresent(filePath, lineN, line, validator, lineid)
        
        return line, skip

    # Process lines which do not have lineid
    def __lineidAbsent(self, filePath, lineN, line, validator):
        sLine = line.strip()

        if validator.validateLineidIsNeeded(sLine, self.boxTrigger):
            gLineid = self.__generateLineid(filePath, lineN, sLine, self.newcompat, validator)
            line = self.incertLineId(line, gLineid)
            skip = False
        else:
            skip = True
        
        return line, skip

    # Process lines which have lineid present
    def __lineidPresent(self, filePath, lineN, line, validator, lineid):
        sLine = line.strip()
        # Check and resolve existing conflicts. Only if (self.resolve != False).
        conflicts = validator.getConflictDic()
        if self.resolve and f"{filePath}_Line{lineN}" in conflicts:
            gLineid = self.__generateLineid(filePath, lineN, sLine, self.resolve, validator)
            skip = False
        # Validate that present lineid comply to user choices.
        # If current lineid valid and unique - leave it untouched
        elif validator.validateHexLength(lineid) == self.compat or not self.compat:
            skip = True
            gLineid = lineid
        else:
            gLineid = self.__generateLineid(filePath, lineN, sLine, self.compat, validator)
            skip = False

        line = self.replaceLineId(line, lineid, gLineid)

        return line, skip
        
    # Cycle of generating lineid until it is of valid length and is unique
    def __generateLineid(self, filePath, lineN, lineText, crcType, validator):
        tryN = 0
       
        lineid = self.__generateCrc(filePath, lineN, lineText, crcType, tryN)

        usedLineids = validator.getLineidUsedDic()
        while lineid in usedLineids or validator.validateHexLength(lineid) != crcType:
            tryN += 1
            lineid = self.__generateCrc(filePath, lineN, lineText, crcType, tryN)
        # Adding to dictionary of used lineids for further conflict identification
        validator.addToLineidUsedDic(lineid, f"{filePath}_Line{lineN}")

        return lineid

    # Resolve on user choice which crc generate (crc24 or crc64) and generate correspondingly
    def __generateCrc(self, filePath, lineN, lineText, crcType, tryN):
        crcString = f"{filePath}{lineN}{lineText}{tryN}"

        if crcType == self.lenYarn:
            crc = self.generateCRC24(crcString)
        elif crcType == self.lenLong:
            crc = self.generateCRC64(crcString)

        return crc

    # Generator of crc24 integers and convert to hex
    @staticmethod
    def generateCRC24(string):
        """
        docstring
        """
        toBytes = string.encode('utf-8')
        crc24 = libscrc.interlaken(toBytes)
        # print(hex(crc24))
        lineid = hex(crc24)[2:]
        return lineid

    # Generator of crc64 integers and convert to hex
    @staticmethod
    def generateCRC64(string):
        """
        docstring
        """
        toBytes = string.encode('utf-8')
        crc64 = libscrc.ecma182(toBytes)
        # print(hex(crc64))
        lineid = hex(crc64)[2:]
        return lineid


    # Incert new LineTag into the line.
    # Currently LineTag(LineId) should be before the Comment\Lore
    @staticmethod
    def incertLineId(line: str, lineid: str) -> str:
        if line.find("//") != -1:
            lineSplit = line.split("//", 1)
            lineidSplit = lineSplit[0].split("#line:")
            if len(lineidSplit) > 2:
                lineidSplit[-1] = lineid
                line = "#line:".join(lineidSplit) + f"//{lineSplit[1]}"
            elif len(lineidSplit) == 1:
                line = f"{line} #line:{lineid} //{lineSplit[1]}"
            else:
                line = lineSplit[0].replace("#line:", f"#line:{lineid}") + f"//{lineSplit[1]}"
        else:
            lineidSplit = line.split("#line:")
            if len(lineidSplit) > 2:
                lineidSplit[-1] = lineid
                line = "#line:".join(lineidSplit)
            elif len(lineidSplit) == 1:
                line = f"{line} #line:{lineid}"
            else:
                line = line.replace("#line:", f"#line:{lineid}")

        return line


    # Replace existing LineTag in the line.
    @staticmethod
    def replaceLineId(line: str, lineidOld: str, lineidNew: str) -> str:
        lineidSplit = line.split(lineidOld)
        if len(lineidSplit) > 2:
            lineidSplit = line.split("#line:")
            lineidSplit[-1] = lineidSplit[-1].replace(lineidOld, lineidNew)
            line = "#line:".join(lineidSplit)
        else:
            line = line.replace(lineidOld, lineidNew)

        return line
