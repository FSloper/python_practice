import json

def load_latest_prize():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    latest_period = max(data.keys(), key=lambda x: int(x))
    prize = data[latest_period].split(',')
    return {
        'red': set(prize[:6]),
        'blue': prize[6],
        'period': latest_period
    }

def get_user_numbers():
    while True:
        try:
            input_str = input("请输入6个红球和1个蓝球（用逗号/空格分隔）: ")
            numbers = [n.strip() for n in input_str.replace('，', ',').split(',') if n.strip()]
            
            if len(numbers) != 7:
                raise ValueError("请输入7个数字（6红+1蓝）")
                
            reds = set(numbers[:6])
            blue = numbers[6]
            
            # 验证红球
            if len(reds) != 6:
                raise ValueError("红球有重复")
            if any(not n.isdigit() or int(n)<1 or int(n)>33 for n in reds):
                raise ValueError("红球应为1-33的数字")
                
            # 验证蓝球
            if not blue.isdigit() or int(blue)<1 or int(blue)>16:
                raise ValueError("蓝球应为1-16的数字")
                
            return {'red': reds, 'blue': blue}
            
        except ValueError as e:
            print(f"输入无效: {e}，请重新输入")
        except Exception as e:
            print(f"发生错误: {str(e)}，请重新输入")

def check_prize(user, prize):
    red_match = len(user['red'] & prize['red'])
    blue_match = user['blue'] == prize['blue']
    
    if red_match == 6:
        return "一等奖" if blue_match else "二等奖"
    elif red_match == 5:
        return "三等奖" if blue_match else "四等奖"
    elif red_match == 4:
        return "四等奖" if blue_match else "五等奖"
    elif red_match == 3:
        return "五等奖" if blue_match else "未中奖"
    elif red_match < 3 and blue_match:
        return "六等奖"
    return "未中奖"

def main():
    prize = load_latest_prize()
    print(f"最新第{prize['period']}期开奖号码：")
    print(f"红球: {', '.join(sorted(prize['red'], key=int))} 蓝球: {prize['blue']}")
    
    user = get_user_numbers()
    result = check_prize(user, prize)
    
    print("\n中奖结果：")
    print(f"红球命中: {len(user['red'] & prize['red'])}个")
    print(f"蓝球{'命中' if user['blue'] == prize['blue'] else '未中'}")
    print(f"中奖等级: {result}")

if __name__ == '__main__':
    while True:
        main()