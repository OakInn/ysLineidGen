import argparse


def prepareOptions(program, description):

    parser = argparse.ArgumentParser(description=description, prog=program)

    parser.add_argument(r"""--BCKP""", help=r"""Path to folder for backing up files in SRC {OPTIONAL,type:string,default:""}""", metavar=r"""BCKP""", dest=r"""BCKP""" , type=str    )
    parser.add_argument(r"""--ext""", help=r"""Extensions of files for procession {OPTIONAL,type:string,default:".txt_.yarn_.yarn.txt"}""", metavar=r"""ext""", dest=r"""ext""" , type=str   , default=r""".txt_.yarn_.yarn.txt""" )
    parser.add_argument(r"""--compat""", help=r"""Initial line tag length check. ""/"yarn"/"long" {OPTIONAL,type:string,default:""}""", metavar=r"""compat""", dest=r"""compat""" , type=str    )
    parser.add_argument(r"""--resolve""", help=r"""Line tag length for conflict resolve. ""/"yarn"/"long" {OPTIONAL,type:string,default:""}""", metavar=r"""resolve""", dest=r"""resolve""" , type=str    )
    parser.add_argument(r"""--newcompat""", help=r"""Newly generated line tag length. "yarn"/"long" {OPTIONAL,type:string,default:"yarn"}""", metavar=r"""newcompat""", dest=r"""newcompat""" , type=str   , default=r"""yarn""" )
    parser.add_argument(r"""--loglevel""", help=r"""Log level, possible values [ERROR|WARNING|INFO|DEBUG] {OPTIONAL,type:string,default:"INFO"}""", metavar=r"""loglevel""", dest=r"""loglevel""" , type=str   , default=r"""INFO""" )

    parser.add_argument(r"""SRC""", type=str,  help=r"""Path to folder which contain yarn spinner files {REQUIRED,type:string}""")

    return parser

def usage(program, description=""):
    return prepareOptions(program, description).format_help()

def parse(program, description, argv, allowIncomplete=False):

    parser = prepareOptions(program, description)

    args = None
    if allowIncomplete:
        args = parser.parse_known_args(argv)
    else:
        args = parser.parse_args(argv)

    return args;
