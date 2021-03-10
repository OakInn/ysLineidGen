# SL_Extractor.py
# SetLineid Extractor class

# Extract from line necessary Text elements - like lineid, comment or text,
# which should be translated.
# "##" - is not a comment, but part of a text



class Extractor:
    def __init__(self):
        pass

    # Extract lineid from the line. If absent - return None
    @staticmethod
    def extractLineid(sLine):
        sLine = sLine.strip().replace("##", "@NotComment@")
        # If line starts with "#" - skip the line, but if line starts with #line: - we need it
        if sLine.find("#line:") == -1 or sLine.startswith("#"):
            return None
        lineidSplit = sLine.split("#line:")

        isLastWord = True
        for i in ["#", " "]:
            if lineidSplit[1].lstrip().find(i) != -1:
                lineidSplit = lineidSplit[1].split(i, 1)
                lineid = lineidSplit[0].strip()
                isLastWord = False
                break
        if isLastWord:
            lineid = lineidSplit[1].strip()

        return lineid

    # Extract comment from the line
    @staticmethod
    def extractComment(line):
        sLine = line.strip()
        comment = ""
        sLine = sLine.strip().replace("##", "@NotComment@")

        lineid = Extractor.extractLineid(sLine)

        if sLine.find("#") != -1:
            commentSplit = sLine.split("#", 1)
            if sLine.startswith("#"):
                comment = commentSplit[1]
            elif sLine.find("#line:") == -1:
                comment = commentSplit[1].strip()
            elif commentSplit[1].startswith("line:"):
                idSplit = sLine.split(f"{lineid}", 1)
                comment = idSplit[1].strip()
                if comment.find("#") != -1:
                    comment = comment.split("#", 1)[1].strip()
            else:
                commentSplit[1] = commentSplit[1].replace(f"#line:{lineid}", "...", 1)
                comment = commentSplit[1].strip()

        try:
            comment = comment.replace("@NotComment@", "##")
        except:
            pass

        return comment