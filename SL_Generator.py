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
# or 2 bytes), but the default setting is that all lineids should be of a yarn
# spinner length (which is 6 characters, or 3 bytes)

import libscrc
from SL_Extractor import Extractor
from SL_Validator import Validator


class Generator:
    def __init__(self, userChoice):
        # Need two user choices - what lineid length (3/8 byte) should be.
        # For both newly created (newcompat) and those already present (compat)
        self.compat = userChoice["compat"]
        self.newcompat = userChoice["newcompat"]
        # User choice, which desides whether to resolve conflicts (duplicate lineid)
        # and in which way (generate new lineid with chosen length - 3/8 bytes)
        self.resolve = userChoice["resolve"]

        self.lenYarn = "yarn"# 3 bytes long lineid
        self.lenLong = "long"# 8 bytes long lineid
        # Variable for controlling persistant behavior
        self.skipTrigger = True

    # Function which should be called for lineid generation
    def generatorProcess(self, filePath, sData, validator):
        # Terminate the program and provide all metrics, warnings and conflicts
        if self.resolve == None and len(validator.getConflictDic()) != 0:# TODO
            pass

        lineN = 0# Line counter

        for line in sData:
            lineN += 1
            # Trigger between node Settings, node Content and skip lines which
            # start with "//" sign. We don't need lineids for Yarn Spinner node
            # Settings (===) and fully commented lines, but need for node Content (---).
            skipLine, validator.idNeeded = self.__skipLineFilter(line)

            if skipLine:
                continue
            else:
                # Decide between skipping or generating lineid for line inside
                # yarn spinner node content
                line, skipLine = self.__lineFilter(filePath, lineN, line, validator)
                if skipLine:
                    continue
            sData[lineN-1] = line

        return sData

    # Skip fully commented and lines in yarn node Settings area - blocks of lines 
    # between "===" and "---" . And skip lines which are requested to be skipped
    def __skipLineFilter(self, line):
        sLine = line.strip()
        skip = True
        vIdNeeded = False
        lineid = Extractor.extractLineid(sLine)

        if not sLine or sLine.startswith("//") or lineid == "skip":
            pass
        elif sLine.startswith("---"):
            vIdNeeded = True
            self.skipTrigger = False
        elif sLine.startswith("==="):
            skip = True
            self.skipTrigger = True
        else:
            if self.skipTrigger:
                skip = True
            else:
                skip = False
                vIdNeeded = True
        
        return skip, vIdNeeded

    # Skip or process lines in yarn node Content area - blocks of lines 
    # between "---" and "==="
    def __lineFilter(self, filePath, lineN, line, validator):
        sLine = line.strip()
        lineid = Extractor.extractLineid(sLine)

        if lineid == None:
            line, skip = self.__lineidAbsent(filePath, lineN, line, validator)

        else:
            line, skip = self.__lineidPresent(filePath, lineN, line, validator, lineid)
        
        return line, skip

    # Process lines which do not have lineid
    def __lineidAbsent(self, filePath, lineN, line, validator):
        sLine = line.strip()

        if validator.validateLineidIsNeeded(sLine):
            gLineid = self.__generateLineid(filePath, lineN, sLine, self.newcompat, validator)
            line = f"{line} #line:{gLineid}"
            skip = False
        else:
            skip = True
        
        return line, skip

    # Process lines which have lineid present
    def __lineidPresent(self, filePath, lineN, line, validator, lineid):
        sLine = line.strip()
        # Check and resolve existing conflicts. Only if (self.resolve != None).
        # If "None", and there are conflicts - program should terminate \
        # after Validator and before Generator class.
        conflicts = validator.getConflictDic()
        if self.resolve != None and f"{filePath}_Line{lineN}" in conflicts:
            gLineid = self.__generateLineid(filePath, lineN, sLine, self.resolve, validator)
            skip = False
        # Validate that present lineid comply to user choices.
        # If current lineid valid and unique - leave it untouched
        elif Validator.validateHexLength(lineid) == self.compat or self.compat == False:
            skip = True
            gLineid = lineid
        else:
            gLineid = self.__generateLineid(filePath, lineN, sLine, self.compat, validator)
            skip = False

        line = line.replace(f"#line:{lineid}", f"#line:{gLineid}", 1)

        return line, skip
        
    # Cycle of generating lineid until it is of valid length and is unique
    def __generateLineid(self, filePath, lineN, lineText, crcType, validator):
        tryN = 0
       
        lineid = self.__generateCrc(filePath, lineN, lineText, crcType, tryN)

        usedLineids = validator.getLineidUsedDic()
        while lineid in usedLineids or Validator.validateHexLength(lineid) != crcType:
            tryN += 1
            lineid = self.__generateCrc(filePath, lineN, lineText, crcType, tryN)
        # Adding to dictionary of used lineids for further conflict identification
        validator.addToLineidUsedDic(lineid, f"{filePath}_Line{lineN}")#?

        return lineid

    # Resolve on user choice which crc generate (crc24 or crc64) and generate correspondingly
    def __generateCrc(self, filePath, lineN, lineText, crcType, tryN):
        crcString = f"{filePath}{lineN}{lineText}{tryN}"

        if crcType == self.lenYarn:
            crc = Generator.generateCRC24(crcString)
        elif crcType == self.lenLong:
            crc = Generator.generateCRC64(crcString)

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