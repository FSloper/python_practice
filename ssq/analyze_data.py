import json

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
from collections import defaultdict

# 读取数据
import argparse

parser = argparse.ArgumentParser(description='双色球数据分析')
parser.add_argument('--input', default='data.json', help='输入数据文件路径')
args = parser.parse_args()

with open(args.input, 'r') as f:
    data = json.load(f)

# 初始化计数器
red_counts = defaultdict(int)
blue_counts = defaultdict(int)

# 统计出现次数
for numbers in data.values():
    parts = numbers.split(',')
    reds = parts[:6]
    blue = parts[6]

    for num in reds:
        red_counts[num] += 1
    blue_counts[blue] += 1

# 计算概率
total = len(data)
red_prob = {k: f'{(v / total) * 100:.3f}%' for k, v in red_counts.items()}
blue_prob = {k: f'{(v / total) * 100:.4f}%' for k, v in blue_counts.items()}

# 生成排序后的红球概率图
sorted_red = sorted(red_prob.items(), key=lambda x: -float(x[1][:-1]))
sorted_nums = [k for k, v in sorted_red]
sorted_probs = [float(v[:-1]) for v in dict(sorted_red).values()]

plt.figure(figsize=(30, 8))
bars = plt.bar(range(len(sorted_red)), sorted_probs, width=0.25)
plt.xticks(range(len(sorted_red)), sorted_nums, rotation=45, fontsize=8)
plt.title('红球号码概率分布（降序排列）')
plt.xlabel('红球号码')
plt.ylabel('出现概率(%)')

# 添加百分比标签
for bar, prob in zip(bars, sorted_probs):
    percent = f"{prob:.4f}%"
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             percent,
             ha='center', va='bottom',
             fontsize=9)

plt.tight_layout(pad=3.0)
plt.savefig('red_ball_probability_sorted.png')

# 生成排序后的蓝球概率图
sorted_blue = sorted(blue_prob.items(), key=lambda x: -float(x[1][:-1]))
sorted_nums = [k for k, v in sorted_blue]
sorted_probs = [float(v[:-1]) for v in dict(sorted_blue).values()]

plt.figure(figsize=(14, 8))
bars = plt.bar(range(len(sorted_blue)), sorted_probs, width=0.6)
plt.title('蓝球号码概率分布（降序排列）')
plt.xlabel('蓝球号码')
plt.ylabel('出现概率(%)')
plt.xticks(range(len(sorted_blue)), sorted_nums, rotation=45)

# 添加百分比标签
for bar, prob in zip(bars, sorted_probs):
    percent = f"{prob:.4f}%"
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             percent,
             ha='center', va='bottom',
             fontsize=9)

plt.tight_layout(pad=3.0)
plt.savefig('blue_ball_probability_sorted.png')
