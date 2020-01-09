# -*- coding: utf-8 -*-

#####################################################################
# File Name:  main.py
# Author: shenming
# Created Time: Mon Jan  6 11:27:41 2020
#####################################################################

import os
import sys
sys.path.insert(0, '..')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from pprint import pprint
import random
import selenium_spider
import string

class BDLiuXY(selenium_spider.SeSpider):
    def __init__(self):
        super(BDLiuXY, self).__init__()
        self.base_url = "https://www.lxybaike.com/"
        self.urls = set()
        self.out = open("test.out", 'w', encoding='utf8')

    def __del__(self):
        # need to call father class destroy method
        # you could comment this to keep the browser.
        #super(BDLiuXY, self).__del__()
        self.out.close()
        pass

    def handle_url(self, url):
        print(url)
        self.urls.add(url)
        self.get_url_until_CLASS(url, "title")
        eles = self.get_multi_class("title")
        for i in eles:
            text = self.get_ele_text(i)
            print(text)
            self.out.write(text+'\n')
        next_url = None
        try:
            fenye = self.get_id("fenye")
            a_tags = fenye.find_elements_by_tag_name("a")
            a_tag = a_tags[-1]
            if self.get_ele_text(a_tag) == "››":
                next_url = self.get_ele_attribute(a_tag, "href")
            # if next_url:
            #     next_url = self.base_url + next_url
        except Exception as e:
            print(repr(e))
            return
        if next_url and next_url not in self.urls:
            self.handle_url(next_url)

    def run(self):
        for i in string.ascii_uppercase:
            url = "https://www.lxybaike.com/index.php?list-letter-{}.html".format(i)
            self.handle_url(url)

if __name__ == "__main__":
    spdier = BDLiuXY()
    spdier.run()
