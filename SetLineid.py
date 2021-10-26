# SetLineid.py
# Setting lineid in yarn/txt files compatible with yarn spinner format.

# Requirements
# Python 3.6 or higher is needed
# pip install libscrc 1.3 - for CRC generation (SL_Generator.py).

# Look through text files, with text in yarn spinner compatible format.
# Analyze each line and decide if line already has lineid, or needs it, or just skip line.
# Skip lines which should be, or have been requested to be skipped ("#line:skip")
# If line already has lineid:
# - check lineid validity - it should be of hex type
# - check lineid uniqueness through all the files
# - check lineid length - depends on user choice:
#       -3 or 8 byte length, or leave as is - as long as it is unique and valid.
# If lineid is absent:
# - check whether it needs one and either skip line, or generate a new valid 
#   and unique lineid of user-chosen length (3/8 bytes)
# - lineid is generated also on user request - when line has empty lineid tag ("#line:").
# Though only in parts of yarn node contents and inside <<box>> sections.

# Run command (recommended)
# python {pathToScript} {pathToFolderWithFiles} --BCKP {pathToFolderForBackups} 

import logging
import sys
import os
from tempfile import gettempdir
import SL_Logger

from SL_Common import Common
from SL_Validator import Validator
from SL_Generator import Generator

from SL_pa import parse


def checkConfig(config):
    if not os.path.exists(config.SRC):
        logging.info(config)
        logging.error(f"Source path does not exist '{config.SRC}'")
        sys.exit(1)
    if not os.path.isdir(config.SRC):
        logging.info(config)
        logging.error(f"Source is not directory '{config.SRC}'")
        sys.exit(1)
    if config.BCKP:
        if not os.path.exists(config.BCKP):
            logging.info(config)
            logging.error(f"Backup folder does not exist '{config.BCKP}'")
            sys.exit(1)
        if not os.path.isdir(config.BCKP):
            logging.info(config)
            logging.error(f"Backup is not directory '{config.BCKP}'")
            sys.exit(1)

    # print configuration
    logging.debug(config) 


if __name__ == '__main__':
    description = """
    Program processes file(s) from provided path(s); creates backup files and
    adds YarnSpinner lineIds to appropriate lines.
    """
    # Arguments processing
    config = parse(os.path.basename(sys.argv[0]), description, sys.argv[1:])
    print(config)

    # initialize logger
    SL_Logger.init(config.loglevel, os.path.normpath(gettempdir()), "sl.log")

    # output configuration
    logging.debug("Arguments parsed")

    # validate required parameters
    logging.debug("Validate configuration")
    checkConfig(config)

    # Parsed arguments
    generatorArguments = {"compat": config.compat, "resolve": config.resolve, "newcompat": config.newcompat}

    v = Validator()
    g = Generator(generatorArguments)
    c = Common()

    path = config.SRC
    backupPath = config.BCKP

    fileExts = config.ext.split("_")

    fileList = c.filePathCollector(path, fileExts)
    fileN = 0
    conflictFiles = 0
    for f in fileList:
        fileN += 1
        c.backupFile(f, backupPath)

        fRead = c.readFile(f)

        v.validatorProcess(f, fRead)

        # Check all files for conflicts (if at least one was found) and provide \
        #   metrics in the end.
        if g.resolve is None and v.conflict:
            print(f"File ({f}) - Conflicts found\n")
            conflictFiles += 1
            continue
        elif g.resolve is None and len(v.getConflictDic()) != 0:
            print(f"File ({f}) [conflict] - OK\n")
            continue
        else:
            genData = g.generatorProcess(f, fRead, v)

            c.writeFile(genData, f)

            print(f"File ({f}) [generated] - OK\n\
            processed {v.lineNFile} lines\n")

    print(f"Total files - {len(fileList)}")
    print(f"Total files processed - {fileN}")
    print(f"Total lines processed - {v.lineNAll}")
    if v.conflictN != 0:
        print(f"Total files with conflicts - {conflictFiles}")
        print(f"Total conflicts found - {v.conflictN}")
        print("CONFLICTS:\n- " + "\n- ".join(f"{k}: {v}" for k,v in v.getConflictDic().items()))