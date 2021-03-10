# SL_Generator_Test.py
# Tests for SL Generator class
#


import unittest
from SL_Generator import Generator
from SL_Validator import Validator


class GeneratorTest(unittest.TestCase):
    def setUp(self):
        userChoice = {"compat": "yarn", "resolve": "long", "newcompat": "yarn"}
        self.g = Generator(userChoice)
        self.v = Validator()

    def testGenerator01GenerateProcess(self):
        filePath = "C:\\Temp\\nonExistant.txt"
        data = """
title: Start
---

    Player: Hey, Sally. #line:34
<<if true>> #line:
    Player: Hey, Sally.                                                         #line:34
Sally: Oh! Hi.
    Sally: You snuck up on me. #comment
Sally: Don't do that.
    <<else>>
Player: Hey.                                                                    #line:305cd
    #Sally: Hi. #line:305cde
<<endif>>
    ===
title: Start
    tags: 
colorID: 2
    position: 567,1160
---
I have [plural {$apples} one="an apple" other="% apples"]!
<<set $monster to "your own hubris">>You accidentally stab yourself with the rock.    
[[Dead]]
<<set $light to "dim">> text <<set $monster to "bear">>
#line: The wind blows softly through the trees. The sound of rustling leaves is reminiscent of the ocean. #line:01 # comment
[[Build a fire|Fire]] #line:02
[[Try to find your way out|Escape]] #line:03
[[Resign to your fate|Dead]] #line:04
===
title: Fire
tags: 
colorID: 1
position: -125,790
---
<<set $light to "bright">>You collect some dry wood and begin to build your campfire.#line:
What do you do now?
<<set $monster to "big strong thing that hates yodeling idk names are hard">>
I'm sorry to inform you that you have died. Our records show that a "$monster" killed you.
[[Yes|Start]] #line:12
===
title: Sleep
tags: 
colorID: 1
position: 707,164
---
<<set $monster to "an even bigger rock with even better clothes">>You find a sturdy stick and the sharp looking rock.

[[This is unacceptable. Destroy the rock.|Dead]]
[[Put the rock down. You will find your own style, eventually.|Fire]] #line:18
[[Turn the rock into a weapon. Poison your enemies with its sick threads.|Weapon]] #line:19
===
title: Weapon
tags: 
colorID: 1
position: 312,114
---
===



title: Start
tags: 
colorID: 2
position: 567,1160
---
<<set $light to "dim">><<set $monster to "bear">>
The wind blows softly through the trees. The sound of rustling leaves is reminiscent of the ocean. The wind gently nips at your ears and nose. You feel both at peace and on edge. These woods are full of monsters and night rapidly approaches. What do you do? #line:01

[[Build a fire|Fire]] #line:02
[[Try to find your way out|Escape]] #line:03
[[Resign to your fate|Dead]] #line:04
===
title: Fire
tags: 
colorID: 1
position: -125,790
---
<<set $light to "bright">>You collect some dry wood and begin to build your campfire. You carefully stack the logs and sprinkle some kindling around for good measure. Once you're satisfied with your craftsmanship, you strike a match and set it all ablaze. #line:05

What do you do now? #line:06
[[Try to get some sleep|Sleep]] #line:07
[[Craft a weapon|Make]] #line:08
<<set $monster to "big strong thing that hates yodeling idk names are hard">>
[[Practice your yodeling|Dead]] #line:09
===
title: Escape
tags: 
colorID: 3
position: 461,799
---
<<set $monster to "something spooky probably">>You fail to escape and die. #line:10
[[Dead]]
===
title: Dead
tags: 
colorID: 5
position: 890,767
---
I'm sorry to inform you that you have died. Our records show that a "$monster" killed you. How unfortunate. Would you like to try again? #line:11
[[Yes|Start]] #line:12
===
title: Sleep
tags: 
colorID: 1
position: 707,164
---
<<if $light is "bright">>It's too bright. You cannot sleep. #line:13
[[Do something else.|Fire]] #line:14
<<else>>
You fall asleep quite peacefully, blissfully unaware of your impending death. #line:15
<<set $monster to "that minecraft monster in the new update that attacks you if you don't sleep for like three days">>
[[Dead]]
<<endif>>
===
title: Make
tags: 
colorID: 1
position: -271,117
---
<<set $monster to "an even bigger rock with even better clothes">>You find a sturdy stick and the sharp looking rock. You ask the rock for fashion advice and where it got those snazzy clothes. The rock does not respond. #line:16

[[This is unacceptable. Destroy the rock.|Dead]] #line:17
[[Put the rock down. You will find your own style, eventually.|Fire]] #line:18
[[Turn the rock into a weapon. Poison your enemies with its sick threads.|Weapon]] #line:19
===
title: Weapon
tags: 
colorID: 1
position: 312,114
---
I have [plural {$apples} one="an apple" other="% apples"]! #line:20
<<set $monster to "your own hubris">>You accidentally stab yourself with the rock. #line:21
[[Dead]]
===

"""

        sData = data.split("\n")

        expectedData = ""

#=================================
        self.v.validatorProcess(filePath, sData)

        cDict = self.v.getConflictDic()
        uDict = self.v.getLineidUsedDic()
        # print(uDict)
        eCDictLen = 7
        with self.subTest(f"{len(cDict)} != Expected {eCDictLen}"):
            self.assertTrue(len(cDict) == eCDictLen)

        eUDictLen = 23
        with self.subTest(f"{len(uDict)} != Expected {eUDictLen}"):
            self.assertTrue(len(uDict) == eUDictLen)
#=================================

        newData = self.g.generatorProcess(filePath, sData, self.v)

        cDict = self.v.getConflictDic()
        uDict = self.v.getLineidUsedDic()

        eCDictLen = 7
        with self.subTest(f"{len(cDict)} != Expected {eCDictLen}"):
            self.assertTrue(len(cDict) == eCDictLen)

        eUDictLen = eUDictLen + eCDictLen + 35
        with self.subTest(f"{len(uDict)} != Expected {eUDictLen}"):
            self.assertTrue(len(uDict) == eUDictLen)

        