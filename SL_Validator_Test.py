# SL_Validator_Test.py
# Tests for SL Validator class
# python v3.6 at least (f-string)
# Functionality tests - HEX type check, adding functions, 

import unittest
from SL_Validator import Validator
from tempfile import gettempdir
from SL_Common import Common
from SL_Generator import Generator


class ValidatorTest(unittest.TestCase):
    def setUp(self):
        self.tempFolderPath = f"{gettempdir()}/"
        self.validator = Validator()


    def testValidator01HexType(self):
        lineId = ["012345", "6789ab0ff1000000", "cdef01", "012f", "6089ghab00000000", "c0d0bf01", "dk02", ""]
        expectedResult = {"012345": True, "6789ab0ff1000000": True, "cdef01": True,\
            "012f": True, "6089ghab00000000": False, "c0d0bf01": True, "dk02": False, "": False}
        
        result = {}
        for i in lineId:
            result[i] = Validator.validateHexType(i)
            with self.subTest(f"{i}:{result[i]} != Expected {i}:{expectedResult[i]}"):
                self.assertTrue(result[i] == expectedResult[i])


    def testValidator02HexLength(self):
        lineids = ["012345", "6789ab0ff1000000", "cdef01", "012f", "6089ghab00000000", "c0d0bf01", "dk02"]
        expectedResult = ["yarn", "long", "yarn", "ownLen", "long", "ownLen", "ownLen"]

        result = []
        index = 0
        for i in lineids:
            result.append(Validator.validateHexLength(i))
            with self.subTest(f"{expectedResult[index]} = {result[index]}"):
                self.assertTrue(expectedResult[index] == result[index])
            index +=1

        with self.subTest(f"{expectedResult} = {result}"):
            self.assertTrue(expectedResult == result)


    def testValidator03LineidIsNeeded(self):
        text = """---
#Player: Hey, Sally.
##Sally: Oh! Hi.
Sally: You snuck up on me.
Sally: Don't#do that.
Player: Hey.
Sally: Hi.
<<set $light to "dim">><<set $monster to "bear">>
[[Build a fire|Fire]]
[[Fire]]
===
title: Weapon
tags: 
colorID: 1
position: 312,114
---
I have [plural {$apples} one="an apple" other="% apples"]!
<<set $monster to "your own hubris">>You accidentally stab yourself with the rock.
->[[Fire]]
<<set $monster to "your own hubris">>You accidentally stab yourself with the rock.>>
<<set $monster to "your own hubris">>You<< accidentally stab yourself with the rock.>>
==="""

        expectedResult = [False, True, True, True, True, True, False, True,
        False, False, False, False, False, True, True, True, True, True]

        result = []
        index = 0
        for line in text.split("\n"):
            if len(line) == 0:
                continue
            elif line.strip().startswith("---"):
                self.validator.idNeeded = True
                continue
            elif line.strip().startswith("==="):
                self.validator.idNeeded = False
                continue
            result.append(self.validator.validateLineidIsNeeded(line))
            with self.subTest(f"{line}:{expectedResult[index]} = {result[index]}"):
                self.assertTrue(expectedResult[index] == result[index])
            index +=1
        
        with self.subTest(f"{expectedResult} = {result}"):
            self.assertTrue(expectedResult == result)
        with self.subTest(f"{len(expectedResult)} = {len(result)}"):
            self.assertTrue(len(expectedResult) == len(result))


    # Test Add functions
    def testValidator04AddFunctions(self):
        v = Validator()
        key = "key"
        value = "value"

        expectedLineidDic = expectedConflictDic = {"key0":"value0", "key1":"value1", "key2":"value2"}
        for i in range(3):
            v.addToLineidUsedDic(f"{key}{i}", f"{value}{i}")
            v.addToConflictDic(f"{key}{i}", f"{value}{i}")
        with self.subTest(f"{v.lineidUsedDic} != {expectedLineidDic}"):
            self.assertTrue(v.lineidUsedDic == expectedLineidDic)
        with self.subTest(f"{v.conflictDic} != {expectedConflictDic}"):
            self.assertTrue(v.conflictDic == expectedConflictDic)


    def testValidator05Process(self):
        testFileName1 = "testValidatorProcess1.txt"
        testText1 = """
#Player: Hey, Sally. #line:794945
##Sally: Oh! Hi. #line:2dc39b
Sally: You snuck up on me. #line:34de2f
Sally: Don't#do that. #line:dcc2bc
Player: Hey. #line:a8e70c
Sally: Hi. #line:305cde
==="""
        testFilePath1 = f"{self.tempFolderPath}{testFileName1}"
        Common.writeFile(testText1.split("\n"), f"{testFilePath1}")
        #=========================================
        testFileName2 = "testValidatorProcess2.txt"
        testText2 = """
Player: Hey, Sally. #line:794946
Sally: Oh! Hi. #line:2dc39c
Sally: You snuck up on me. #line:34de2f
Sally: Don't#do that. #line:dcc2be
Player: Hey. #line:a8e70d
Sally: Hi. #line:305cde
==="""
        testFilePath2 = f"{self.tempFolderPath}{testFileName2}"
        Common.writeFile(testText2.split("\n"), f"{testFilePath2}")


        pathList = [testFilePath1, testFilePath2]
        for p in pathList:
            sData = Common.readFile(p)
            self.validator.validatorProcess(p, sData)


        expectedLineNAll = 16
        with self.subTest(F"{self.validator.lineNAll} != Expected {expectedLineNAll}"):
            self.assertTrue(self.validator.lineNAll == expectedLineNAll)

        # print(self.validator.getLineidUsedDic())
        expectedLineidUsedDic = {"2dc39b": f"{testFilePath1}_Line3","34de2f": f"{testFilePath1}_Line4",\
            "dcc2bc": f"{testFilePath1}_Line5", "a8e70c": f"{testFilePath1}_Line6",\
                "305cde": f"{testFilePath1}_Line7", "794946": f"{testFilePath2}_Line2",\
                    "2dc39c": f"{testFilePath2}_Line3", "dcc2be": f"{testFilePath2}_Line5",\
                        "a8e70d": f"{testFilePath2}_Line6"}
        with self.subTest(f"{len(self.validator.lineidUsedDic)} != Expected {len(expectedLineidUsedDic)}"):
            self.assertTrue(len(self.validator.lineidUsedDic) == len(expectedLineidUsedDic))
        for l in self.validator.lineidUsedDic:
            with self.subTest(f"{self.validator.lineidUsedDic[l]} != Expected {expectedLineidUsedDic[l]}"):
                self.assertTrue(self.validator.lineidUsedDic[l] == expectedLineidUsedDic[l])
        

        expectedConflictN = 2
        with self.subTest(f"{self.validator.conflictN} != Expected {expectedConflictN}"):
            self.assertTrue(self.validator.conflictN == expectedConflictN)


        expectedComflictDic = {f"{testFilePath2}_Line4": f"conflict with {expectedLineidUsedDic['34de2f']}",\
            f"{testFilePath2}_Line7": f"conflict with {expectedLineidUsedDic['305cde']}"}
        with self.subTest(f"{len(self.validator.conflictDic)} != Expected {len(expectedComflictDic)}"):
            self.assertTrue(len(self.validator.conflictDic) == len(expectedComflictDic))
        with self.subTest(f"{self.validator.conflictDic} != Expected {expectedComflictDic}"):
            self.assertTrue(self.validator.conflictDic == expectedComflictDic)
        for c in self.validator.conflictDic:
            with self.subTest(f"{self.validator.conflictDic[c]} != Expected {expectedComflictDic[c]}"):
                self.assertTrue(self.validator.conflictDic[c] == expectedComflictDic[c])


    def testValidator06Getters(self):
        v = Validator()

        expectedEmptyDic = 0
        expectedEmptyDic2 = {}
        with self.subTest(f"{v.getConflictDic()} != Expected {expectedEmptyDic2}"):
            self.assertEqual(v.getConflictDic(), expectedEmptyDic2)
        with self.subTest(f"{len(v.getLineidUsedDic())} != Expected {expectedEmptyDic}"):
            self.assertEqual(len(v.getLineidUsedDic()), expectedEmptyDic)

        expectedLineidDic = {"lineid1":"lineid1", "lineid2":"lineid2", "lineid3":"lineid3"}
        for i in range(1, 4):
            v.lineidUsedDic[f"lineid{i}"] = f"lineid{i}"
        with self.subTest(f"{v.getLineidUsedDic()} != Expected {expectedLineidDic}"):
            self.assertEqual(v.getLineidUsedDic(), expectedLineidDic)
        
        expectedConflictDic = {"conflict1":"conflict1", "conflict2":"conflict2", "conflict3":"conflict3"}
        for i in range(1, 4):
            v.conflictDic[f"conflict{i}"] = f"conflict{i}"
        with self.subTest(f"{v.getConflictDic()} != Expected {expectedConflictDic}"):
            self.assertEqual(v.getConflictDic(), expectedConflictDic)
