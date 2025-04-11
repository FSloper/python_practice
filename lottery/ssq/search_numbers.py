import json
import argparse


def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("错误：未找到data.json文件")
        exit(1)


def parse_numbers(input_str):
    numbers = input_str.replace(',', ' ').split()
    # 统一格式为两位数，不足补零
    return [n.zfill(2) for n in numbers]


def find_matches(data, reds, blue=None):
    matches = []
    for qihao, numbers in data.items():
        nums = numbers.split(',')
        target_reds = sorted(nums[:6])
        input_reds = sorted(reds)
        
        # 完全匹配模式（需要蓝球）
        if blue:
            if len(input_reds) == 6 and len(blue) == 1:
                if input_reds == target_reds and blue[0] == nums[6]:
                    matches.append(qihao)
        # 模糊查询模式（仅红球）
        else:
            if input_reds == target_reds:
                matches.append(qihao)
    return matches


def main():
    parser = argparse.ArgumentParser(description='双色球号码查询工具')
    parser.add_argument('-n', '--numbers', help='输入号码，用空格/逗号分隔（6红球或6+1）')
    args = parser.parse_args()
    
    data = load_data()
    
    if args.numbers:
        input_numbers = args.numbers
    else:
        input_numbers = input("请输入号码（6个红球或6红+1蓝，用空格/逗号分隔）: ")
    
    numbers = parse_numbers(input_numbers)
    
    if len(numbers) not in [6, 7]:
        print("错误：请输入6个红球或6红球+1蓝球")
        return
    
    reds = numbers[:6]
    blue = numbers[6:] if len(numbers) ==7 else None
    
    matches = find_matches(data, reds, blue)
    
    if matches:
        print(f"找到 {len(matches)} 条匹配结果：")
        for qihao in matches:
            print(f"期号：{qihao}  号码：{data[qihao]}")
    else:
        print("未找到匹配的期号")


if __name__ == '__main__':
    main()