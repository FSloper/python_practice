import json

import requests

qeury_url = ('http://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?'
             'name=ssq&'
             'issueCount=&'
             'issueStart=&'
             'issueEnd=&'
             'dayStart=&'
             'dayEnd=&'
             'pageNo=1&'
             'pageSize=10&'
             'week=&'
             'systemType=PC')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    # 模拟浏览器标识
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  # 可接受的内容类型
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',  # 语言偏好
    'Accept-Encoding': 'gzip, deflate, br',  # 支持的压缩格式
    'Connection': 'keep-alive',  # 保持长连接
    'Referer': 'https://www.cwl.gov.cn/',  # 来源页面（用于反爬）
    'Content-Type': 'application/json',  # 请求体格式（POST/PUT时需设置）
    'Authorization': 'Bearer your_token_here',  # 身份验证（如JWT）
    'Cookie': 'session_id=abc123; user_pref=dark_mode'  # Cookie信息（需动态获取）
}
json_response = requests.get(qeury_url, headers=headers, verify=False).text
json_response_result = json.loads(json_response)['result']
print(json_response_result)

# 读取现有数据
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

new_data = {}
added_count = 0

# 遍历所有获取的期数（按从新到旧顺序）
for issue in json_response_result:
    if issue['code'] not in data:
        numbers = f"{issue['red']},{issue['blue']}"
        new_data[issue['code']] = numbers
        added_count += 1

if new_data:
    # 合并旧数据（保留原有顺序）
    new_data.update(data)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print(f"成功添加 {added_count} 期新数据")
else:
    print("没有需要更新的新数据")