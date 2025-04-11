import json
from collections import defaultdict

def validate_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("错误：未找到data.json文件")
        return

    # 获取文件最后修改时间
    import os
    file_mtime = os.path.getmtime('data.json')
    from datetime import datetime
    print(f"数据文件最后修改时间：{datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d %H:%M:%S')}")

    # 验证期号格式和唯一性
    valid_format = []
    invalid_qihao = []
    qihao_set = set()
    duplicates = []

    for qihao in data.keys():
        # 格式验证：7位数字，前4位是年份，后3位是序号
        if not (qihao.isdigit() and len(qihao) == 7):
            invalid_qihao.append(qihao)
            continue
        
        # 唯一性验证
        if qihao in qihao_set:
            duplicates.append(qihao)
        else:
            qihao_set.add(qihao)

    # 按年份分组期号
    year_groups = defaultdict(list)
    for qihao in data.keys():
        year = qihao[:4]
        seq = int(qihao[4:])
        year_groups[year].append(seq)

    # 验证连续性
    broken_sequences = []
    for year, seqs in year_groups.items():
        sorted_seqs = sorted(seqs)
        for i in range(1, len(sorted_seqs)):
            if sorted_seqs[i] != sorted_seqs[i-1] + 1:
                prev_qihao = f"{year}{sorted_seqs[i-1]:03d}"
                current_qihao = f"{year}{sorted_seqs[i]:03d}"
                broken_sequences.append({
                    'year': year,
                    'missing_between': [prev_qihao, current_qihao],
                    'missing_count': sorted_seqs[i] - sorted_seqs[i-1] - 1
                })

    # 输出结果
    print("数据验证结果：")
    print(f"重复期号总数：{len(duplicates)}")
    if duplicates:
        print("重复期号列表：", ", ".join(duplicates))
    
    print(f"\n断号问题总数：{len(broken_sequences)}")
    for issue in broken_sequences:
        print(f"年份 {issue['year']}: 在 {issue['missing_between'][0]} 和 {issue['missing_between'][1]} 之间缺少 {issue['missing_count']} 期")

if __name__ == '__main__':
    validate_data()