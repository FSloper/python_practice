import json
import pandas as pd
from collections import defaultdict

# 读取JSON数据
with open('ssq/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 生成纯数字列标题（01-49）
columns = ['期号'] + [f"{i:02d}" for i in range(1, 50)]

# 准备数据存储
excel_data = []

# 处理每期数据
for issue, numbers in data.items():
    row = defaultdict(str)
    row['期号'] = issue
    
    all_numbers = numbers.split(',')
    reds = all_numbers[:6]
    blue = all_numbers[6]
    
    # 填充红球（01-33列）
    for r in reds:
        row[r.zfill(2)] = r.zfill(2)  # 在对应列填入号码
        
    # 填充蓝球（34-49列对应蓝球01-16）
    blue_col = f"{33 + int(blue):02d}"  # 将蓝球号码映射到34-49列
    row[blue_col] = blue.zfill(2)
    
    excel_data.append(row)

# 创建DataFrame并保持列顺序
df = pd.DataFrame(excel_data, columns=columns)

# 保存Excel文件
df.to_excel('ssq/ssq_results.xlsx', index=False)