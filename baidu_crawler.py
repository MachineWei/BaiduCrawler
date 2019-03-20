# -*- coding: utf-8 -*-
"""
爬虫：从百度汉语中爬取词语拼音、解释、近义词、反义词
"""

import random
import time
import requests
from bs4 import BeautifulSoup

words = ['高兴', '悲伤']  # 待爬词语，根据需要个人定制
Len_ = len(words)

success = []
omission = []
count = 0

for m in range(len(words)):
    temp = []
    temp.append(words[m])
    url = 'https://hanyu.baidu.com/s?wd=' + words[m] + '&ptype=zici'
    try:
        response = requests.get(url)
        content = response.content.decode()
        soup = BeautifulSoup(content, "lxml")

        pinyin_dt = soup.find(name='dt', class_='pinyin')
        pinyin = pinyin_dt.get_text().replace(' ', '')
        temp.append(pinyin)

        meaning_div = soup.find(name='div', class_='tab-content')
        meaning = meaning_div.get_text().replace('\n', '').replace(' ', '')
        meaning = meaning.replace(pinyin, '')
        temp.append(meaning)

        onym_div = soup.find_all(name='div', class_='block')
        synonym = onym_div[0].get_text().replace(' ', '').split('\n')
        synonym = '|'.join([i for i in synonym if i != ''])
        antonym = onym_div[1].get_text().replace(' ', '').split('\n')
        antonym = '|'.join([i for i in antonym if i != ''])
        temp.append(synonym)
        temp.append(antonym)

        success.append(temp)
    except:
        omission.append(words[m])

    count += 1
    print("第"+str(count)+'个已完成')
    sleep = random.uniform(0.5, 1.5)
    time.sleep(sleep)
    if count % 100 == 0:
        rate_ = round(count/Len_, 2)*100
        print("总体已完成"+str(rate_)+"%的数据爬取。")

# 爬取成功的词语写入excel文件
import os
import time
import xlwt

path = r'C:\Users\Win\Desktop'
workbook = xlwt.Workbook(encoding = 'utf-8')
excel_sheet_name = time.strftime('%Y%m%d')
worksheet = workbook.add_sheet(excel_sheet_name)

worksheet.write(0, 0, label = '词语')
worksheet.write(0, 1, label = '拼音')
worksheet.write(0, 2, label = '释义')
worksheet.write(0, 3, label = '近义词')
worksheet.write(0, 4, label = '反义词')

for i in range(len(success)):
    for j in range(len(success[i])):
        worksheet.write(i+1, j, label = success[i][j])

outfile_name = excel_sheet_name + '词语爬虫success.xls'
file_path = os.path.join(path, outfile_name)
workbook.save(file_path)

# 未爬取成功的词语写入本地txt
omission_file = excel_sheet_name + '词语爬虫omission.txt'
omission_path = os.path.join(path, omission_file)
with open(omission_path,'w',encoding='utf-8') as f:
    for i in omission:
        f.write(i+'\n')

print('全部词语意思爬取完成，请检查未爬取成功词语omission.txt')


