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

#ENCODING = "gb18030"
ENCODING = "utf8"

#########################small utils##################################
def tp(ss):
    '''
    终端输出
    '''
    sys.stdout.buffer.write((ss+'\n').encode(ENCODING))

def read_sum_dict(ff):
    '''
    读取sum.dict
    return dict type
    '''
    c_dict = {}
    for i in open(ff, encoding = ENCODING):
        ii = i.strip().split()
        word = ii[0].split('(')[0].strip()
        if word == '</s>' or word == '</s>' or word == '<unk>' or word == 'SL':
            continue
        if not word:
            continue
        pron = ' '.join(ii[1:])
        pron = pron.replace(" [ wb ]", "")
        if word in c_dict:
            c_dict[word].append(pron)
            c_dict[word].sort()
        else:
            c_dict[word] = [pron]
    return c_dict

def read_pplm_dcit(ff):
    '''
    读取pplm.dict
    return set type
    '''
    ss = set()
    for i in open(ff):
        ii = i.strip().split('\t')
        if len(ii) == 1:
            continue
        ss.add(ii[1])

def output_sum_dict(total_dict, ff):
    '''
    input:
        total_dict DICT
    sum.dict文件生成
    '''
    out = open(ff, 'w', encoding = ENCODING)
    list_dict = sorted(total_dict.items())
    out.write("{}\n".format("<s>(01)             SIL [ wb ]"))
    out.write("{}\n".format("</s>(01)             SIL [ wb ]"))
    out.write("{}\n".format("SL(01)             SIL [ wb ]"))
    out.write("{}\n".format("<unk>(01)             SIL [ wb ]"))
    for i in list_dict:
        word =i[0]
        pron = list(set(i[1]))
        pron.sort()
        for p in range(len(pron)):
            pp = pron[p].split()
            if len(pp) == 1:
                pp.append("[ wb ]")
            else:
                pp.insert(1, "[ wb ]")
                pp.append("[ wb ]")
            out.write("{}({:0>2})            {}\n".format(word, p+1, " ".join(pp)))
    out.close()

def strQ2B(str):
    '''
    全角转半角
    '''
    r_str = ""
    for char in str:
        inside_code=ord(char)
        if inside_code == 12288:  # 全角空格
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):
            inside_code -= 65248
        r_str += chr(inside_code)
    return r_str

def strB2Q(str):
    '''
    半角转全角
    '''
    r_str = ""
    for char in str:
        inside_code=ord(char)
        if inside_code == 32:
            inside_code = 12288
        elif (inside_code >= 33 and inside_code <= 126):
            inside_code += 65248
        r_str += chr(inside_code)
    return r_str

def is_contain_Q_Char(str):
    '''
    判断文本是否包含全角字符，普通字符除外
    '''
    for char in str:
        inside_code = ord(char)
        if inside_code == 12288 or (inside_code >= 65281 and inside_code <= 65347):
            return True
    return False

#####################################################################

class Base:
    def __init__(self, argv):
        if len(argv) == 0 or argv[0] == 'h' :
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

class BDMergeSumDict(Base):
    '''
    合并两个sum.dict
    '''
    def __init__(self, argv):
        super(BDMergeSumDict, self).__init__(argv)
        self.dict1 = argv[0]
        self.dict2 = argv[1]
        self.dict_out = argv[2]

    def print_help(self):
        print("python {} -c {} sum.dict1 sum.dict2 sum.dict.out".format(sys.argv[0], __class__.__name__))

    def run(self):
        cc_dict1 = read_sum_dict(self.dict1)
        cc_dict2 = read_sum_dict(self.dict2)
        total_dict = {}
        for k in cc_dict1:
            if k not in cc_dict2:
                total_dict[k] = cc_dict1[k]
            else:
                pron_list = cc_dict1[k] + cc_dict2[k]
                total_dict[k] = pron_list
        output_sum_dict(total_dict, self.dict_out)

class BDFilterSumDictByPPLMDict(Base):
    '''
    根据 pplm.dict 过滤sum.dict
    '''
    def __init__(self, argv):
        super(BDFilterSumDictByPPLMDict, self).__init__(argv)
        self.sum_dict = argv[0]
        self.pplm_dict = argv[1]
        self.sum_out = argv[2]

    def print_help(self):
        print("python {} -c {} sum.dict pplm.dict sum.dict.out".format(sys.argv[0], __class__.__name__))

    def run(self):
        cc_dict = read_sum_dict(self.sum_dict)
        words_set = read_pplm_dcit(self.pplm_dict)
        new_dict = {}
        for k in cc_dict:
            if k in word_set:
                new_dict[k] = cc_dict[k]
        output_sum_dict(new_dict, self.sum_out)

class SMQJBJHandle(Base):
    '''
    判断文件是否包含全角字符
    文件全角字符转半角
    文件半角字符转全角
    '''
    def __init__(self, argv):
        super(SMQJBJHandle, self).__init__(argv)
        self.file = argv[0]
        if len(argv) >= 2:
            self.out_file = argv[1]
            self.type = int(argv[2])
            if self.type != 1 and self.type != 2:
                raise ValueError("type need to be {1 : Q2B; 2 :  B2Q}")
        else:
            self.out_file  =None

    def print_help(self):
        print("python3 {} -c {} input_file [output_file {{1 : Q2B; 2 :  B2Q}}]".format(sys.argv[0], __class__.__name__))

    def run(self):
        if not self.out_file:
            line_count = 0
            for i in open(self.file, 'r', encoding=ENCODING):
                line_count += 1
                ii = i.strip()
                if is_contain_Q_Char(ii):
                    print("file {} contain QUANJIAO character in line {}\n{}".format(self.file, line_count, ii))
                    sys.exit(0)
            print("file {} contain no QUANJIAO character")
        else:
            out = open(self.out_file, 'w', encoding=ENCODING)
            for i in open(self.file, 'r', encoding=ENCODING):
                if self.type == 1:
                    new_sen = strQ2B(i)
                else:
                    new_sen = strB2Q(i)
                out.write(new_sen)


GLOBAL_DICT = {
    "BDFilterListByAns" : BDFilterListByAns,
    "BDExtractWrongFromWer" : BDExtractWrongFromWer,
    "BDMergeSumDict" : BDMergeSumDict,
    "BDFilterSumDictByPPLMDict" : BDFilterSumDictByPPLMDict,
    "SMQJBJHandle" : SMQJBJHandle,
}

def print_global_help():
    global GLOBAL_DICT
    help_str = "SMTools.py [-h] [-c CLASSNAME]\n\navailable classname:\n"
    for key in GLOBAL_DICT:
        help_str += "\t"
        help_str += key + "\n"
        doc = GLOBAL_DICT[key].__doc__.strip().replace("\n", "\n    ");
        help_str += "\t"
        help_str += doc + "\n\n"
    tp(help_str)


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
