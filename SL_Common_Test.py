# SL_Common_Test.py
# python v3.6 at least (f-string)
# Tests for SL Common class
# Functionality tests - read file, backup file, write file,
# list of file pathes found by extension

import os
from tempfile import gettempdir
import unittest
from SL_Common import Common

class CommonTest(unittest.TestCase):
    def setUp(self):
        self.testFileName = "testFile.ttxt"
        self.tempFolderPath = f"{gettempdir()}/"
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
        self.testFilePath = f"{self.tempFolderPath}{self.testFileName}"
        self.testFileCreate = Common.writeFile(self.testText.split("\n"), f"{self.testFilePath}")


    def testCommon01Backup(self):
        fileForBackup = self.testFilePath
        backupPath = f"{self.tempFolderPath}testFileBackup.txt.fc"

        expectedPath = f"{self.tempFolderPath}testFileBackup.txt.fc"
        
        backup = Common.backupFile(fileForBackup, backupPath)

        with self.subTest(f"00. File exist - {expectedPath}"):
            self.assertTrue(os.path.exists(f"{expectedPath}"))
        with self.subTest(f"01. Content is the same - {Common.readFile(fileForBackup)}"):
            self.assertTrue(Common.readFile(backupPath))


    def testCommon02ReadFile(self):
        filepath = self.testFilePath

        expectedNLines = 14
        expectedTextInLine8 = "Sally: Don't do that. #line:dcc2bc"
        expectedData = self.testText.split("\n")

        readFile = Common.readFile(filepath)

        with self.subTest(f"00. {len(readFile)} != Expected {expectedNLines}"):
            self.assertTrue(len(readFile) == expectedNLines)
        with self.subTest(f"01. {readFile[8]} != Expected {expectedTextInLine8}"):
            self.assertTrue(readFile[8] == expectedTextInLine8)
        with self.subTest(f"02. {readFile} != Expected {expectedData}"):
            self.assertTrue(readFile == expectedData)


    def testCommon03WriteFile(self):
        writeData = self.testText.split("\n")
        writePath = f"{self.tempFolderPath}testWriteDataInThisFile.ttxt"

        expectedData = writeData
        expectedlen = len(writeData)#14

        writeFile = Common.writeFile(writeData, writePath)
        readFile = Common.readFile(writePath)

        with self.subTest(f"00. No file - {writePath}"):
            self.assertTrue(os.path.exists(str(writePath)))
        with self.subTest(f"01. {len(readFile)} != Expected {expectedlen}"):
            self.assertTrue(len(readFile) == expectedlen)
        with self.subTest(f"02. {readFile} != Expected {expectedData}"):
            self.assertTrue(readFile == expectedData)


    def testCommon04FilePathCollector(self):
        file1 = f"{self.tempFolderPath}testFile.ttxt"
        file2 = f"{self.tempFolderPath}testWriteDataInThisFile.ttxt"
        file3 = f"{self.tempFolderPath}testFileBackup.txt.fc"
        folderPath = self.tempFolderPath
        searchFileByExtension = (".ttxt", ".fc")

        expectedFileList = (file1, file2, file3)

        fileList = []
        for i in range(len(searchFileByExtension)):
            ext = searchFileByExtension[i]
            foundFileList = Common.filePathCollector(folderPath, ext)
            if i < len(searchFileByExtension):
                fileList = fileList + foundFileList
        fileList = tuple(fileList)
        
        with self.subTest(f"\n00. {len(fileList)} != Expected {len(expectedFileList)}"):
            self.assertTrue(len(fileList) == len(expectedFileList))
        with self.subTest(f"\n01. {fileList} != Expected {expectedFileList}"):
            self.assertTrue(fileList == expectedFileList)