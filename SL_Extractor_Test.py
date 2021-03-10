# SL_Extractor_Test.py
# python v3.6 at least (f-string)
# Tests for SL Extractor class
# Functionality tests - extract lineid,


import unittest
from SL_Extractor import Extractor

class ExtractorTest(unittest.TestCase):
    def setUp(self):
        pass

    def test01ExtractLineid(self):
        sData = """
        #Player: Good lord!!! WTF? #line:bacd12
        Sally: WTF was that "WTF" for? #Need to think about the language here for kids sake
        ##Sally: Don't swear on me here! Kids! #line:abcd12
        Player: Our car is gone!!! #line:abcd13 #think here as well
        Sally: Kids, shut your ears! WTF did you just say?! #line:ab01
        Player: Our car is gone!!! #line:abcd14 #line:abcd15
        Player: Our car is gone!!! ##line:abcd16 #line:abcd17
        Player: Our car is gone!!! ###line:abcd18 #line:abcd19
        Player: Our car is gone!!! ##line:abcd20 ##line:abcd21
        Player: Our car is gone!!! #line:abcd22   ##line:      abcd23
        Player: Our car is gone!!! #line:#line:1
        Player: Our car is gone!!! #line: da23#line:"""

        expectedLineid = [None, None, None, "abcd12", "abcd13", "ab01", "abcd14",\
            "abcd17", "abcd18", None, "abcd22", "", "da23"]

        for i in range(len(expectedLineid)):
            lineid = Extractor().extractLineid(sData.split("\n")[i])
            with self.subTest(f"{lineid} != Expected {expectedLineid[i]}"):
                self.assertTrue(lineid == expectedLineid[i])

    
    def test02ExtractComment(self):
        sData = """
        #
        #.
        #...
        #05: fully commented with text and lineid #line:bacd12
        06: partially commented. #Comment simple
        ##07: no comment ##07, double hash with lineid #line:abcd12
        08: Simple and correct line with lineifd and comment #line:abcd13 #Comment
        09: Comment and lineid without spaces#line:abcd13#Comment
        10: Comment and lineid lots of spaces     #line:      abcd13#Comment
        11:Sally: Yo! # comment
        12:Sally: Yo! #line:xxxxxx # comment
        13:Sally: Yo! #comment #line:xxxxxx # comment
        14:Sally: Yo! #comment #line:xxxxxx
        15:Sally: Yo! #comment #line:xxxxxx # comment #line:yyyyyy
        16:Sally: Yo! #comment #line: # comment #line:
        17:Sally: Yo! #line:xxxxxx comment
        #line:ab01 #Sally: Kids, shut your ears! WTF did you just say?! #line:ab01
        """

        expectedComment = ["", "", ".", "...", "05: fully commented with text and lineid #line:bacd12",
        "Comment simple", "", "Comment", "Comment", "Comment", "comment", "comment",
        "comment ... # comment", "comment ...", "comment ... # comment #line:yyyyyy", 
        "comment ... # comment #line:", "comment", "line:ab01 #Sally: Kids, shut your ears! WTF did you just say?! #line:ab01"]

        for i in range(len(expectedComment)):
            comment = Extractor.extractComment(sData.split("\n")[i])
            with self.subTest(f"line{i}:{comment} != Expected {expectedComment[i]}"):
                self.assertTrue(comment == expectedComment[i])