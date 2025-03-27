import json
from collections import defaultdict

import pandas as pd
from openpyxl.styles import Alignment


def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_probability(numbers, total):
    return round((numbers / total) * 100, 2)

def process_red_balls(data):
    red_counts = {}
    red_consecutive = defaultdict(int)
    red_max_consecutive = defaultdict(int)
    last_appearance = {}  # 新增：记录最后出现期号
    sorted_periods = sorted(data.keys(), key=lambda x: int(x))  # 按期号排序
    max_period = int(sorted_periods[-1]) if sorted_periods else 0  # 最新期号

    for period in sorted_periods:
        current_period = int(period)
        numbers = data[period]
        current_reds = set(numbers.split(',')[:6])
        
        # 更新连续出现次数
        for num in red_counts:
            if num in current_reds:
                red_consecutive[num] += 1
            else:
                red_consecutive[num] = 0
            red_max_consecutive[num] = max(red_max_consecutive[num], red_consecutive[num])
        
        # 更新出现次数
        for num in current_reds:
            red_counts[num] = red_counts.get(num, 0) + 1
        
        # 新增：更新最后出现期号
        for num in current_reds:
            last_appearance[num] = current_period
    
    total_periods = len(data)
    total = sum(red_counts.values())
    
    # 在DataFrame中添加新列
    df = pd.DataFrame([(
        k, 
        v, 
        total_periods / (v + 1),
        red_max_consecutive[k],
        calculate_probability(v, total),
        max_period - last_appearance[k]  # 新增列计算
    ) for k, v in red_counts.items()],
    columns=pd.Index(['号码', '出现次数', '平均遗漏', '最大连出', '概率(%)', '距上次出现期数']))  # 修改为pd.Index
    
    # 在生成DataFrame前添加区间统计
    interval_stats = {
        '1-11': sum(v for k, v in red_counts.items() if 1 <= int(k) <= 11),
        '12-22': sum(v for k, v in red_counts.items() if 12 <= int(k) <= 22),
        '23-33': sum(v for k, v in red_counts.items() if 23 <= int(k) <= 33)
    }
    total = sum(interval_stats.values())
    avg_ratio = sum(interval_stats[k]/total for k in interval_stats) / 3
    
    # 创建区间统计DataFrame
    df_interval = pd.DataFrame({
        '区间': list(interval_stats.keys()) + ['平均比值'],
        '出现次数': list(interval_stats.values()) + [None],
        '比值平均值': [v/total for v in interval_stats.values()] + [avg_ratio]
    })

    # 在生成DataFrame前添加位置平均值统计
    position_sums = [0] * 6  # 存储6个位置的数字总和
    total_periods = len(data)
    
    for period in sorted_periods:
        numbers = list(map(int, data[period].split(',')[:6]))  # 转换为整数列表
        for i in range(6):
            position_sums[i] += numbers[i]
    
    # 计算每个位置的平均值并保留3位小数
    position_avg = [round(total / total_periods, 3) for total in position_sums]
    
    # 创建位置统计DataFrame
    df_position = pd.DataFrame({
        '位置': [f'第{i+1}位' for i in range(6)],
        '平均值': position_avg
    })

    return df.sort_values('号码').reset_index(drop=True), df_interval, df_position

def process_blue_balls(data):
    blue_counts = {}
    blue_consecutive = defaultdict(int)
    blue_max_consecutive = defaultdict(int)
    last_appearance = {}
    sorted_periods = sorted(data.keys(), key=lambda x: int(x))
    
    # 改用期号索引位置计算期数差
    period_index = {p: idx for idx, p in enumerate(sorted_periods, 1)}  # 期号到顺序位置的映射
    total_periods = len(sorted_periods)

    for period in sorted_periods:
        current_period = int(period)
        numbers = data[period]
        # 确保蓝球号码统一为两位数格式
        current_blue = f"{int(numbers.split(',')[6]):02d}"  # 修改为更可靠的格式化方式
        
        # 更新连续出现次数
        for num in blue_counts:
            if num == current_blue:
                blue_consecutive[num] += 1
            else:
                blue_consecutive[num] = 0
            blue_max_consecutive[num] = max(blue_max_consecutive[num], blue_consecutive[num])
        
        # 更新出现次数和最后出现期号
        blue_counts[current_blue] = blue_counts.get(current_blue, 0) + 1
        # 记录当前期号的位置索引
        last_appearance[current_blue] = period_index[period]  # 改为存储顺序位置
    
    # 在for循环之后添加总数计算
    total = sum(blue_counts.values())  # 添加总数计算
    
    # 修改DataFrame构造部分
    # 新增蓝球平均值计算
    blue_sum = 0
    for period in sorted_periods:
        numbers = data[period].split(',')
        blue_sum += int(numbers[6])  # 提取第七位数值
    
    # 在现有DataFrame添加平均值行
    df = pd.DataFrame([(
        k, v, 
        total_periods / (v + 1),
        blue_max_consecutive[k],
        calculate_probability(v, total),
        period_index[sorted_periods[-1]] - last_appearance[k]
    ) for k, v in blue_counts.items()] + [
        ('平均值', '', '', '', round(blue_sum/total_periods, 3), '')
    ], columns=pd.Index(['号码', '出现次数', '平均遗漏', '最大连出', '概率(%)', '距上次出现期数']))

    return df.sort_values('号码').reset_index(drop=True)

def create_excel(red_original, blue_df):
    with pd.ExcelWriter('statistics.xlsx', engine='openpyxl') as writer:
        red_df, red_interval, red_position = red_original
        
        red_df.to_excel(writer, sheet_name='红球统计', index=False)
        red_interval.to_excel(writer, sheet_name='红球区间统计', index=False)
        red_position.to_excel(writer, sheet_name='红球位置统计', index=False)
        
        # 设置位置统计表的数字格式
        sheet = writer.book['红球位置统计']
        for row in sheet.iter_rows(min_row=2, max_row=7, min_col=2, max_col=2):
            cell = row[0]
            cell.number_format = '0.000'
        blue_df.to_excel(writer, sheet_name='蓝球统计', index=False)
        
        # 设置单元格格式
        workbook = writer.book
        for sheetname in writer.sheets:
            sheet = workbook[sheetname]
            for row in sheet.iter_rows(min_row=2):
                cell = row[0]
                cell.number_format = '00'
                cell.alignment = Alignment(horizontal='center')

def main():
    data = load_data()
    red_df, red_interval, red_position = process_red_balls(data)
    blue_df = process_blue_balls(data)
    create_excel((red_df, red_interval, red_position), blue_df)
    print("统计结果已成功导出到 statistics.xlsx")

if __name__ == '__main__':
    main()