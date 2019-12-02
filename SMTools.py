# -*- coding: utf-8 -*-

#####################################################################
# File Name:  SMTools.py
# Author: shenming
# Created Time: Mon Dec  2 17:28:55 2019

# collect some tools in work
#####################################################################

import os
import sys
import argparse

ENCODING = "gb18030"

class Base:
    def __init__(*argv):
        pass

    def run():
        pass

class BDFilterListByAns(Base):
    '''
    根据答案文件，对音频列表文件进行简单过滤
    '''
    def __init__(self, argv):
        print(argv)
        if argv[0] == 'h':
            print("python {} -c {} ans.file list.file list.file.new".format(sys.argv[0], __class__.__name__))
            sys.exit(0)
        self.ans_file = argv[0]
        self.list_file = argv[1]
        self.new_file = argv[2]

    def run(self):
        filename_set = set()
        for i in open(self.ans_file, encoding = ENCODING):
            ii = i.strip().split("\t")
            if len(ii) == 2:
                filename_set.add(ii[0])
        out = open(self.new_file, 'w', encoding = ENCODING)
        for  i in open(self.list_file, encoding = ENCODING):
            ii = i.strip()
            if ii in filename_set:
                out.write("{}\n".format(ii))

LIST_HELP = """\
available classname:
    BDFilterListByAns
"""

GLOBAL_DICT = {
    "BDFilterListByAns" : BDFilterListByAns,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="personal tools")
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        print(LIST_HELP)
        sys.exit(0)
    parser.add_argument("-c", "--classname", type=str, help = "classname")
    FLAGS, unparsed = parser.parse_known_args()
    classname = FLAGS.classname
    if classname not in GLOBAL_DICT:
        print(LIST_HELP)
        sys.exit(0)
    worker = GLOBAL_DICT[classname](unparsed)
    worker.run()
