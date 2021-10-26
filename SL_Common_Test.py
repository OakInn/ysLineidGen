# SL_Common_Test.py
# python v3.6 at least (due to f-string)
# Tests for SL Common class
# Functionality tests - read file, backup file, write file,\
# list of file pathes found by extension

import os
from tempfile import gettempdir
import unittest
from SL_Common import Common

class CommonTest(unittest.TestCase):
    def setUp(self):
        self.common = Common()
        self.testFileName = "testFile.ttxt"
        self.tempFolderPath = gettempdir()
        self.testText = """
title: Start
---

<<if true>>
Player: Hey, Sally. #line:794945
Sally: Oh! Hi. #line:2dc39b
Sally: You snuck up on me. #line:34de2f
Sally: Don't do that. #line:dcc2bc
<<else>>
Player: Hey. #line:a8e70c
Sally: Hi. #line:305cde
<<endif>>
==="""
        self.testFilePath = os.path.join(self.tempFolderPath, self.testFileName)
        self.testFileCreate = self.common.writeFile(self.testText.split("\n"), f"{self.testFilePath}")

    def tearDown(self) -> None:
        file = f"{self.testFilePath}.fc_1.fc"
        if os.path.exists(file):
            os.remove(file)
        return super().tearDown()


    def testCommon01Backup(self):
        fileForBackup = self.testFilePath
        backupPath = self.tempFolderPath

        expectedPath = os.path.join(self.tempFolderPath, f"{self.testFileName}.fc")
        backup = self.common.backupFile(fileForBackup, backupPath)

        with self.subTest(f"00. File exist - {expectedPath}"):
            self.assertTrue(os.path.exists(f"{expectedPath}"))
        with self.subTest(f"01. Content is the same - {self.common.readFile(fileForBackup)}"):
            self.assertTrue(self.common.readFile(expectedPath))


    def testCommon02ReadFile(self):
        filepath = self.testFilePath

        expectedNLines = 14
        expectedTextInLine8 = "Sally: Don't do that. #line:dcc2bc"
        expectedData = self.testText.split("\n")

        readFile = self.common.readFile(filepath)

        with self.subTest(f"00. {len(readFile)} != Expected {expectedNLines}"):
            self.assertTrue(len(readFile) == expectedNLines)
        with self.subTest(f"01. {readFile[8]} != Expected {expectedTextInLine8}"):
            self.assertTrue(readFile[8] == expectedTextInLine8)
        with self.subTest(f"02. {readFile} != Expected {expectedData}"):
            self.assertTrue(readFile == expectedData)


    def testCommon03WriteFile(self):
        writeData = self.testText.split("\n")
        writePath = f"{self.tempFolderPath}/testWriteDataInThisFile.ttxt"

        expectedData = writeData
        expectedlen = len(writeData)#14

        writeFile = self.common.writeFile(writeData, writePath)
        readFile = self.common.readFile(writePath)

        with self.subTest(f"00. No file - {writePath}"):
            self.assertTrue(os.path.exists(str(writePath)))
        with self.subTest(f"01. {len(readFile)} != Expected {expectedlen}"):
            self.assertTrue(len(readFile) == expectedlen)
        with self.subTest(f"02. {readFile} != Expected {expectedData}"):
            self.assertTrue(readFile == expectedData)

    # Commented lines below valid for testing recursion.
    def testCommon04FilePathCollector(self):
        file1 = os.path.join(self.tempFolderPath, "testFile.ttxt")
        file2 = os.path.join(self.tempFolderPath, "testWriteDataInThisFile.ttxt")
        file3 = os.path.join(self.tempFolderPath, "testFile.ttxt.fc")
        # file4 = os.path.join(self.tempFolderPath, "testCommon", "testWriteDataInThisFile.ttxt")
        folderPath = self.tempFolderPath
        searchFileByExtension = (".ttxt", ".fc")

        expectedFileList = (file1, file3, file2)
        # expectedFileList = (file1, file2, file3, file4)

        fileList = tuple(self.common.filePathCollector(folderPath, searchFileByExtension))
        
        with self.subTest(f"\n00. {len(fileList)} != Expected {len(expectedFileList)}"):
            self.assertTrue(len(fileList) == len(expectedFileList))
        with self.subTest(f"\n01. {fileList} != Expected {expectedFileList}"):
            self.assertTrue(sorted(fileList) == sorted(expectedFileList))