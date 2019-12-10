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
    def __init__(self, argv):
        if argv[0] == 'h' or len(argv) == 0:
            self.print_help()
            sys.exit(0)

    def run(self):
        pass

    def print_help(self):
        pass

class BDExtractWrongFromWer(Base):
    '''
    从wer文件中获取错误对，wer文件格式和encoding可能不同，需要注意
    '''
    def __init__(self, argv):
        global ENCODING
        ENCODING = "utf8"

        super(BDExtractWrongFromWer, self).__init__(argv)
        self.wer_file = argv[0]
        self.out_file = argv[1]

    def print_help(self):
        print("python {} -c {} wer.file out.file".format(sys.argv[0], __class__.__name__))

    def process_str(self, ss):
        ss = ss.strip()
        ss = ss.split()
        ss = ''.join(ss)
        ss = ss.replace('*', '')
        return ss

    def run(self):
        out = open(self.out_file, 'w', encoding=ENCODING)
        for i in open(self.wer_file, encoding=ENCODING):
            ii = i.strip()
            if ii.startswith("id: "):
                filename = ii[4:]
                continue
            if ii.startswith("Scores ("):
                if ii.endswith("0 0 0"):
                    match_flag = True
                else:
                    match_flag = False
                continue
            if ii.startswith("REF: "):
                ans = ii[5:]
                ans = self.process_str(ans)
                continue
            if ii.startswith("HYP: "):
                dec = ii[5:]
                dec = self.process_str(dec)
                if not match_flag:
                    out.write("{}\t{}\n".format(ans, dec))


class BDFilterListByAns(Base):
    '''
    根据答案文件，对音频列表文件进行简单过滤
    '''
    def __init__(self, argv):
        super(BDFilterListByAns, self).__init__(argv)
        self.ans_file = argv[0]
        self.list_file = argv[1]
        self.new_file = argv[2]

    def print_help(self):
        print("python {} -c {} ans.file list.file list.file.new".format(sys.argv[0], __class__.__name__))

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


GLOBAL_DICT = {
    "BDFilterListByAns" : BDFilterListByAns,
    "BDExtractWrongFromWer" : BDExtractWrongFromWer,
}

def print_global_help():
    global GLOBAL_DICT
    help_str = "available classname:\n"
    for key in GLOBAL_DICT:
        help_str += "\t"
        help_str += key + "\n"
        doc = GLOBAL_DICT[key].__doc__.strip();
        help_str += "\t"
        help_str += doc + "\n\n"
    print(help_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="personal tools")
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        print_global_help()
        sys.exit(0)
    parser.add_argument("-c", "--classname", type=str, help = "classname")
    FLAGS, unparsed = parser.parse_known_args()
    classname = FLAGS.classname
    if classname not in GLOBAL_DICT:
        print_global_help()
        sys.exit(0)
    worker = GLOBAL_DICT[classname](unparsed)
    worker.run()
