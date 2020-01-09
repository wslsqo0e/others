import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from pprint import pprint
import random
import selenium_spider

class BDHanYu(selenium_spider.SeSpider):
    def __init__(self):
        super(BDHanYu, self).__init__()

    def __del__(self):
        # need to call father class destroy method
        # you could comment this to keep the browser.
        super(BDHanYu, self).__del__()
        #pass

    def extract_data(self, out_list):
        while True:
            data = self.get_id("data-container")
            items = data.find_elements_by_css_selector(".poem-list-item")
            for i in items:
                divs = i.find_elements_by_tag_name("div")
                word_div = divs[0]
                word = self.get_ele_text(word_div)
                pinyin_div = divs[1]
                pinyin = self.get_ele_text(pinyin_div)
                print(word, pinyin)
                #out.write("{}\t{}\n".format(word, pinyin))
                out_list.append("{}\t{}".format(word, pinyin))
            try:
                ele = self.driver.find_element_by_css_selector(".paginationjs-next.J-paginationjs-next")
                ele.click()
                time.sleep(2)
            except Exception as e:
                break


    def run(self, word, out):
        word = "{}组词".format(word)
        url = "https://hanyu.baidu.com"
        self.get_url_until_ID(url, "kw")
        ele = self.get_id("kw")
        self.ele_input(ele, word)
        time.sleep(1)
        ele = self.get_id("su")
        self.ele_click(ele)
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "poem-tags-container")))
        except Exception as e:
            try:
                element = self.get_id("copyright")
                return
            except Exception as ne:
                raise e

        eles = self.get_multi_class("poem-tag-type")
        next_links = []
        for i in eles:
            if self.get_ele_text(i) == "拼音:":
                poem_valid = i.find_element_by_xpath('..')
                poem = poem_valid.find_element_by_css_selector(".poem-tags-content.fold")
                next_links = poem.find_elements_by_css_selector(".poem-tag")
                break
        news_links = []
        word_tag = "+{}".format(word)
        print("+{}".format(word), end="")
        if len(next_links) > 0:
            for i in next_links:
                news_links.append(self.get_ele_attribute(i, "href"))
                py = self.get_ele_text(i)
                word_tag += "\t{}".format(py) 
                print("\t{}".format(py), end="")
        word_tag += '\n'
        print()
        print(news_links)
        out_list = []
        self.extract_data(out_list)
        for i in news_links[1:]:
            self.get_url(i)
            time.sleep(2)
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "poem-tags-container")))
            self.extract_data(out_list)
        out.write(word_tag)
        for i in out_list:
            out.write(i+'\n')
        out.flush()

def read_word_list(filename):
    word_list = []
    for i in open(filename, encoding='utf8', errors='ignore'):
        ii = i.strip()
        word_list.append(ii)
    return word_list


if __name__ == "__main__":
    out = open(sys.argv[2], 'w', encoding='utf8')
    word_list = read_word_list(sys.argv[1])
    pp = BDHanYu()
    #word_list = ['崴']
    #word_list = ['了']
    #word_list = ['国']
    retry_count = 0
    for i in word_list:
        while True:
            try:
                pp.run(i, out)
                break
            except Exception as e:
                print('{} retry failed xxxx'.format(retry_count))
                print(repr(e))
                retry_count += 1
                if retry_count >= 3:
                    sys.exit(1)
                else:
                    del pp
                    print("sleep 60 seconds")
                    time.sleep(60)
                    pp = BDHanYu()
                continue
