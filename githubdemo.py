import os
import re
import time
from pprint import pprint
from random import choice
import pymysql
import requests
from lxml import etree
from selenium import webdriver
from setting import User_Agent_list, MYSQL_HOST, MYSQL_PORT, MYSQL_USERNAME, MYSQL_PASSWORK, MYSQL_DATABASE
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyvirtualdisplay import Display
LOG_DIRECTORY = "./"

class Print(object):
    @staticmethod
    def info(message):
        out_message =  Print.timeStamp() + '  ' + 'INFO: ' +str(message)
        Print.write(out_message)
        print(out_message)

    @staticmethod
    def write(message):
        log_path = os.path.join(LOG_DIRECTORY, 'log.txt')
        with open(log_path,'a+') as f:
            f.write(message)
            f.write('\n')

    @staticmethod
    def timeStamp():
        local_time = time.localtime(time.time())
        return time.strftime("%Y_%m_%d-%H_%M_%S", local_time)


class GithubStart(object):
    def __init__(self, url):
        self.opt = webdriver.ChromeOptions()
        self.opt.add_argument('user-agent="{}"'.format(choice(User_Agent_list)))
        self.opt.add_argument('--disable-dev-shm-usage')
        self.opt.add_argument('--no-sandbox')
        display = Display(visible=0, size=(800, 600))
        display.start()
        ##
        self.opt.add_argument('--disable-dev-shm-usage')
        self.opt.add_argument('--no-sandbox')
        # self.proxy = requests.get('http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=0&city=0&yys=0&port=1&time=2&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=')
        # self.opt.add_argument('--proxy-server=http://{}'.format(self.proxy.text))
        # self.prefs = {"profile.managed_default_content_settings.images": 2}
        # self.opt.add_experimental_option("prefs", self.prefs)
        self.opt.add_argument('--headless')
        self.broser = webdriver.Chrome(options=self.opt)
        self.wait = WebDriverWait(self.broser, 20, 0.5)

        self.connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USERNAME,
            password=MYSQL_PASSWORK,
            db=MYSQL_DATABASE,
            charset='utf8'
        )
        self.login_url = 'https://github.com/login'
        self.project_url = url
        self.num = 0

    def get_follow_url(self, url):
        follower_url_list = []
        res = requests.get(url)
        etree_data = etree.HTML(res.text)
        try:
            for i in range(1, 30):
                follower_url = 'https://github.com' + etree_data.xpath('//*[@id="repos"]/ol/li[{}]/div[2]/h3/span/a/@href'.format(i))[0]
                follower_url_list.append(follower_url)

            return follower_url_list
        except:
            return False

    def run(self):

        # 登陆操作
        Print.info('正在登陆')
        self.broser.get(self.login_url)
        username = '569857936@qq.com'
        passwork = 'gyl8838055'
        username_element = self.wait.until(EC.presence_of_element_located((By.NAME, "login")))
        username_element.send_keys(username)

        passwork_element = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        passwork_element.send_keys(passwork)

        self.broser.find_element_by_name('commit').click()

        # 请求项目start页面
        Print.info('正在获取star者url')
        follower_url_list = []
        self.broser.get(self.project_url)
        datas = self.get_follow_url(self.project_url)
        if not datas is False:
            for data in datas:
                follower_url_list.append(data)

        while True:
            try:
                next_element = self.broser.find_element_by_link_text("Next")
                next_url = next_element.get_attribute('href')
                self.broser.get(next_url)
                datas = self.get_follow_url(next_url)
                for data in datas:
                    follower_url_list.append(data)
                Print.info('含有信息 {} 条'.format(len(follower_url_list)))
            except Exception as f:
                break

        # follow 页面提取信息
        Print.info('正在筛选符合条件的人')
        for url in follower_url_list:
            cur = self.connection.cursor()
            self.broser.get(url)
            time.sleep(1)
            self.num +=1
            Print.info('正在处理第 {} 条信息'.format(self.num))
            try:
                email = self.broser.find_element_by_class_name('u-email ').get_attribute('href')
                email = re.search(r'mailto:(.*)', email).group(1)
                nike_name = self.broser.find_element_by_css_selector('[class="p-nickname vcard-username d-block"]').text
                address = self.broser.find_element_by_class_name('p-label').text
                header_img = self.broser.find_element_by_xpath('//*[@id="js-pjax-container"]/div/div[1]/a').get_attribute('href')
                project = re.search(r'https://github.com/(.*)/(.*)/stargazers', self.project_url).group(2)
                homepage_url = url

                if email and address:
                    sql = 'insert into tb_spider_github(nike_name, header_img, address, email, project, homepage_url) values ("%s", "%s", "%s", "%s", "%s", "%s")' % (nike_name, header_img, address, email, project, homepage_url)
                    cur.execute(sql)
                    self.connection.commit()
                    Print.info('添加:{},邮箱:{} 到数据库当中'.format(nike_name, email))
                else:
                    Print.info('不符合要求')

            except Exception as f:
                pass

        Print.info('筛选完毕')
        self.broser.quit()


if __name__ == '__main__':
    # url = input('爬取的项目url：')
    projetclist = [
        'https://github.com/youzan/vant-weapp/stargazers'
    ]
    for project in projetclist:
        obj = GithubStart(project)
        obj.run()