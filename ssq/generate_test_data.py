import json
import random
from datetime import datetime, timedelta


def generate_sample_data(entries=10000000000):
    data = {}
    years = range(2003, 2024)  # 双色球从2003年开始
    for year in years:
        # 生成全年153期数据
        for week in range(1, 154):
            # 生成随机日期（每年1月1日到12月31日之间）
            random_day = datetime(year, 1, 1) + timedelta(days=random.randint(0, 364))
            
            # 生成红球（1-33不重复）
            reds = random.sample(range(1, 34), 6)
            # 生成蓝球（1-16）
            blue = random.randint(1, 16)
            
            # 格式化期号和号码
            date_str = random_day.strftime('%Y-%m-%d')
            qihao = f"{year}-{week:03d}"
            numbers = ','.join([f"{n:02d}" for n in sorted(reds)] + [f"{blue:02d}"])
            
            data[qihao] = numbers
    
    return data

if __name__ == "__main__":
    test_data = generate_sample_data()
    with open('test_data.json', 'w') as f:
        json.dump(test_data, f, indent=2)
    print("成功生成10000条测试数据到test_data.json")