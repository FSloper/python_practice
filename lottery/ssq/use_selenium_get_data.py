from selenium.webdriver.common.by import By
from selenium import webdriver
import re

browser = webdriver.Chrome()
browser.get('https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/')

element=browser.find_element(by=By.CLASS_NAME,value='main-container-content')
content = element.text

# 匹配日期和后面的7个数字
pattern = r'(\d{7})\s+(\d{4}-\d{2}-\d{2}\([日四二]\))\s+([\d\s]+)'
matches = re.findall(pattern, content)

for match in matches:
    print(f"期号: {match[0]}, 开奖日期: {match[1]}")
    numbers = match[2].split()
    print("开奖号码:", " ".join(numbers[:7]))

