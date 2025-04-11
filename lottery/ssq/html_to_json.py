import json
from bs4 import BeautifulSoup

with open('data.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

results = {}

for tr in soup.select('tr[data-alias="undefined"]'):
    tds = tr.find_all('td')
    if len(tds) < 3:
        continue
    
    qihao = tds[0].text.strip()
    # 提取红球（前6个红球）
    reds = [div.text.zfill(2) for div in tr.select('div.qiu-item-wqgg-zjhm-red')[:6]]
    # 提取蓝球（第7个div）
    blue = tr.select_one('div.qiu-item-wqgg-zjhm-blue').text.zfill(2)
    
    # 组合号码并用逗号分隔
    numbers = ','.join(reds + [blue])
    
    results[qihao] = numbers

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"成功转换{len(results)}期数据到data.json")