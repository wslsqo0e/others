import sys
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


"""
User Agent: 用户代理，Http协议中一部分，属于头域的组成部分。其作用是向访问网站提供你所使用的浏览器类型及版本、操作系统及版本、
            浏览器内核等标识信息。通过这个标识，网站可以显示不同的排版从而为用户提供更好的体验或者进行信息统计。
"""

class SeSpider:
    def __init__(self):
        chrome_options = Options()
        # 手机的user_agent
        #user_agent = 'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'

        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        # 0 ==> default  1 ==> allow  2 ==> block
        # block image
        prefs = {"profile.managed_default_content_settings.images": 0}
        chrome_options.add_argument("user-agent=" + user_agent )
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(chrome_options=chrome_options)


    def __del__(self):
        self.driver.close()

    def get_url(self, url):
        self.driver.get(url)

    def get_url_until_TAG(self, url, tag_name):
        """
        等待url加载特定tag完毕
        """
        if not isinstance(tag_name, str):
            print("tag_name need to be string")
            return None
        try:
            self.driver.get(url)
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, tag_name)))
        except Exception as e:
            print(repr(e))
            print("Failed {}".format(url))
            return None
        elem = self.driver.find_element_by_tag_name(tag_name)
        return elem

    def get_url_until_ID(self, url, id_name):
        """
        等待url加载特定ID完毕
        """
        if not isinstance(id_name, str):
            print("id_name need to be string")
            return None
        try:
            self.driver.get(url)
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, id_name)))
        except Exception as e:
            print(repr(e))
            print("Failed {}".format(url))
            return None
        elem = self.driver.find_element_by_id(id_name)
        return elem

    def get_url_until_CLASS(self, url, class_name):
        """
        等待url加载特定CLASS完毕
        """
        if not isinstance(class_name, str):
            print("class_name need to be string")
            return None
        try:
            self.driver.get(url)
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        except Exception as e:
            print(repr(e))
            print("Failed {}".format(url))
            return None
        elem = self.driver.find_element_by_class_name(class_name)
        return elem

    # get element(s) ref: https://selenium-python.readthedocs.io/locating-elements.html
    def get_id(self, id_name):
        return self.driver.find_element_by_id(id_name)

    def get_name(self, name):
        return self.driver.find_element_by_name(name)

    def get_multi_name(self, name):
        return self.driver.find_elements_by_name(name)

    def get_class(self, class_name):
        return self.driver.find_element_by_class_name(class_name)

    def get_multi_class(self, class_name):
        return self.driver.find_elements_by_class_name(class_name)

    def get_tag_name(self, tag_name):
        return self.driver.find_element_by_tag_name(tag_name)

    def get_multi_tag_name(self, tag_name):
        return self.driver.find_elements_by_tag_name(tag_name)

    def get_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def get_multi_xpath(self, xpath):
        return self.driver.find_elements_by_xpath(xpath)

    def get_ele_attribute(self, ele, attr_name):
        if not isinstance(ele, webdriver.remote.webelement.WebElement):
            return None
        return ele.get_attribute(attr_name)

    def get_ele_text(self, ele):
        if not isinstance(ele, webdriver.remote.webelement.WebElement):
            return None
        return ele.text

    def ele_input(self, ele, text):
        """
        NOTE: user responsible for checking whether the element accept the text
        """
        if not isinstance(ele, webdriver.remote.webelement.WebElement):
            raise Exception("ele not webdriver.remote.webelement.WebElement")
        ele.clear()
        ele.send_keys(text)

    def ele_click(self, ele):
        """
        NOTE: user responsible for checking if the element clickable
        """
        ele.click()

    def run(self):
        #self.driver.get("http://www.baidu.com")
        print("father run")

# Example class
# python 中类继承是个伪继承，必须显示的调用了父类的构造函数，才会存在父类实例
class Example(SeSpider):
    def __init__(self):
        super(Example, self).__init__()

    def __del__(self):
        # need to call father class destroy method
        # you could comment this to keep the browser.
        #super(Example, self).__del__()
        pass

    def run(self):
        #self.get_url("http://www.baidu.com")
        self.get_url_until_CLASS("http:///www.baidu.com", "a")
        aas = self.get_multi_tag_name("a")
        ss = self.get_ele_attribute(aas[0], 'href')
        print(ss)
        ss = self.get_ele_text(aas[0])
        print(ss)


if __name__ == "__main__":
    ss = Example()
    ss.run();
    time.sleep(3);
