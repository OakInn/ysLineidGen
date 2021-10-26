# SL_Extractor.py
# SetLineid Extractor class

# Extract from line necessary Text elements:
# - Lineid
# - Comment
# - ...



class Extractor:
    def __init__(self):
        pass

    # Extract lineid from the line. If absent - return None
    @staticmethod
    def extractLineid(line):
        sLine = line.strip()
        # Next two lines mostly needed for tests
        if sLine.find("#line:") == -1 or sLine.startswith("//"):
            return None
        # Comment is the last element in line
        if sLine.find("//") != -1:
            sLine = sLine.split("//", 1)[0].strip()

        lineidSplit = sLine.split("#line:")
        for i in ["//", " "]:# TODO these are not all variants
            if lineidSplit[-1].strip().find(i) != -1:
                return None

        return lineidSplit[-1].strip()   


    # Extract comment from the line
    @staticmethod
    def extractComment(line):
        sLine = line.strip()
        comment = ""
        
        if sLine.find("//") != -1:
            commentSplit = sLine.split("//", 1)
            if sLine.startswith("//") or commentSplit[1].find("#line:") == -1:
                comment = commentSplit[1]
            else:
                lineidSplit = commentSplit[1].split("#line:")
                for i in ["//", " "]:# TODO these are not all variants
                    if lineidSplit[-1].strip().find(i) != -1:
                        comment = commentSplit[1]
                        return comment

                comment = "#line:".join(lineidSplit[:len(lineidSplit)-1])
        return comment