import re

import requests
from lxml import etree

# 所有地区医院列表地址
url = 'http://www.a-hospital.com/w/%E5%85%A8%E5%9B%BD%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8'

resp = requests.get(url)

eroot = etree.HTML(resp.text)
hospitals = eroot.xpath('//b/a/text()')

item = {}
# 获取所有医院列表名字，用于拼接关键字地址
for hospital in hospitals:
    # 省
    item['province'] = re.search(r'(.*)医院列表', hospital).group(1)

    # 获取所有区信息
    area = 'http://www.a-hospital.com/w/' + hospital
    resp = requests.get(area)
    eroot = etree.HTML(resp.text)
    # 所有区列表
    areas = eroot.xpath('//*[@id="bodyContent"]/p[2]/a/text()')
    # 所有区列表地址
    areas_urls = eroot.xpath('//*[@id="bodyContent"]/p[2]/a/@href')

    # 请求每个区地址获取区里所有医院
    for areas_url in areas_urls:
        # 区
        item['area'] = areas[areas_urls.index(areas_url)]

        url = 'http://www.a-hospital.com/' + areas_url
        resp = requests.get(url)
        eroot = etree.HTML(resp.text)

        # 所有医院信息
        hospitals_info = eroot.xpath('//*[@id="bodyContent"]/ul[3]//li')
        for i in hospitals_info:
            print(i.xpath('./text()'))