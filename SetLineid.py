# SetLineid.py
# Setting lineid in yarn file compatible with yarn spinner format.

# Look through .yarn and .txt files, with text in yarn spinner compatible format.
# Analyze each line and decide if line already has lineid, or needs it, or just skip line.
# If line already has lineid:
# - check lineid validity - it should be of hex type
# - check lineid uniqueness through all the files
# - check lineid length - depends on user choice:
#       -3 or 8 byte length, or leave as is - as long as it is unique and valid
# If lineid is absent:
# -check whether it needs one and either skip line, or generate a new valid 
# and unique lineid of user chosen length (3/8 bytes)
# - lineid is generated also on user request - when line has empty lineid tag ("#line:").
# Though only in parts of yarn node contents


from SL_Common import Common
from SL_Validator import Validator
from SL_Generator import Generator

if __name__ == '__main__':

    # Arguments processing
    # Base class??:
        # Common - collect all file paths
        # for each file path
            # Metrics().fileCount += 1
            # Common - read files
            # Validator - Common.getFilename, extract lineid, validate lineid -> conflictStorage
        # if --resolve == no
            # send data to metrics and end the program
    generatorArguments = {"compat": "yarn", "resolve": "long", "newcompat": "yarn"}

    v = Validator()
    g = Generator(generatorArguments)

    path = "D:\\Projects\\Yarn\\Sample\\SetLineid\\"
    backupPath = None

    fileExt = {".txt", ".yarn"}
    fileList = []

    for ext in fileExt:
        files = Common.filePathCollector(path, ext)
        fileList = fileList + files

    print(f"File list = {fileList}\n")

    for f in fileList:
        Common.backupFile(f, backupPath)

        fRead = Common.readFile(f)

        v.validatorProcess(f, fRead)

        # Terminate the program and provide all metrics, warnings and conflicts.
        # Here or in Generator?

        genData = g.generatorProcess(f, fRead, v)

        Common.writeFile(genData, f)

        print(f"File ({f}) - OK\n\
        processed {v.lineNFile} lines\n")

    print(f"Total files processed - {len(fileList)}")
    print(f"Total lines processed - {v.lineNAll}")
    print(f"Total conflicts found - {v.conflictN}")
    if v.conflictN != 0:
        print(v.getConflictDic())