# SL_Extractor_Test.py
# python v3.6 at least (due to f-string)
# Tests for SL Extractor class
# Functionality tests:
# - Extract lineid
# - Extract comment


import unittest
from SL_Extractor import Extractor

class ExtractorTest(unittest.TestCase):
    def setUp(self):
        self.extract = Extractor()

    def test01ExtractLineid(self):
        sData = """
        //Player: Good Lord!!! #line:bacd12
        Sally: Ha? //Need to think about the language here for kids sake
        Sally: Don't call Him in vain! Kids! #line:abcd12
        Player: Our car is gone!!! #line:abcd13 //think here as well
        Sally: Kids, shut your ears! What did you just say?! #line:ab01
        Player: Our car is gone!!! #line:abcd14 //line:abcd15
        Player: Our car is gone!!! line:abcd16 #line:abcd17
        Player: Our car is gone!!! #line:abcd18 //line:abcd19
        Player: Our car is gone!!! line:abcd20 line:abcd21
        Player: Our car is gone!!! #line:abcd22   line:      abcd23
        Player: Our car is gone!!! #line://line:1
        Player: Our car is gone!!! #line: da23//line:

        #line:000001
        tale #line:000001
        author: phrase #line:000001
        author: phrase #line:000001 // comment
        author: phrase // comment #line:000001
        author: phrase // comment #line:000001 comment
        author: phrase // comment #line:000001 // comment
        author: phrase #line:000001 phrase #line:000002 // comment
        author: phrase #line:000001 #line:000002 // comment
        author: phrase #line:000001 [raw][/raw] // comment #line:000002
        author: phrase #line:000001 // comment #line:000002
        author: phrase #line:000001 phrase #line: // comment
        author: phrase #line:000001 #line: // comment
        author: phrase #line:// comment #line:"""

        # expectedLineid = [None, None, None, "abcd12", None, "ab01", None,\
        #     "abcd17", None, None, None, None, None,\
        #     None, "000001", "000001", "000001", None, "000001", None, None, None, None,\
        #     "000002", "000002", None, None, ""]

        expectedLineid = [None, None, None, "abcd12", "abcd13", "ab01", "abcd14",\
            "abcd17", "abcd18", None, None, "", "da23", None,\
            "000001", "000001", "000001", "000001", None, None, None, "000002", "000002", None,\
            "000001", "", "", ""]
       
        for i in range(len(expectedLineid)):
            lineid = self.extract.extractLineid(sData.split("\n")[i])
            with self.subTest(str(sData.split("\n")[i]) + "\n" +f"{lineid} != Expected {expectedLineid[i]}"):
                self.assertTrue(lineid == expectedLineid[i])

    
    def test02ExtractComment(self):
        sData = """
        //
        //.
        //...
        //05: fully commented with text and lineid #line:bacd12
        06: partially commented. //Comment simple
        07: no comment 07, double hash with lineid #line:abcd12
        08: Simple and correct line with lineifd and comment #line:abcd13 //Comment
        09: Comment and lineid without spaces#line:abcd13//Comment
        10: Comment and lineid lots of spaces     #line:      abcd13//Comment
        11:Sally: Yo! // comment
        12:Sally: Yo! #line:xxxxxx // comment
        13:Sally: Yo! //comment #line:xxxxxx // comment
        14:Sally: Yo! //comment #line:xxxxxx
        15:Sally: Yo! //comment #line:xxxxxx // comment #line:yyyyyy
        16:Sally: Yo! //comment #line: // comment #line:
        17:Sally: Yo! #line:xxxxxx //comment
        #line:ab01 //Sally: Kids, shut your ears! What did you just say?! #line:ab01

        #line:000001
        tale #line:000001
        author: phrase #line:000001
        author: phrase #line:000001 // comment
        author: phrase // comment #line:000001
        author: phrase // comment #line:000001 comment
        author: phrase // comment #line:000001 // comment
        author: phrase #line:000001 phrase #line:000002 // comment
        author: phrase #line:000001 #line:000002 // comment
        author: phrase #line:000001 [raw][/raw] // comment #line:000002
        author: phrase #line:000001 // comment #line:000002
        author: phrase #line:000001 phrase #line: // comment
        author: phrase #line:000001 #line: // comment
        author: phrase #line:// comment #line:"""

        expectedComment = ["", "", ".", "...", "05: fully commented with text and lineid #line:bacd12",
        "Comment simple", "", "Comment", "Comment", "Comment", " comment", " comment",
        "comment #line:xxxxxx // comment", "comment ", "comment #line:xxxxxx // comment ", 
        "comment #line: // comment ", "comment", "Sally: Kids, shut your ears! What did you just say?! ",\
        "", "", "", "", " comment", " comment ", " comment #line:000001 comment", " comment #line:000001 // comment",\
        " comment", " comment", " comment ", " comment ", " comment", " comment", " comment "]

        for i in range(len(expectedComment)):
            comment = self.extract.extractComment(sData.split("\n")[i])
            with self.subTest(f"line{i+1}:{comment} != Expected {expectedComment[i]}"):
                self.assertTrue(comment == expectedComment[i])