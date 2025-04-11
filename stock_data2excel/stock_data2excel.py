import json
import random
import secrets
import time

import pandas as pd
import requests
from openpyxl.styles import Alignment, Font


def jquery_mock_callback():
    jQuery_Version = "3.5.1"
    timestamp = int(round(time.time() * 1000))
    return "jQuery" + (jQuery_Version + str(random.random())).replace(".", "") + "_" + str(
        timestamp - 1000)


def get_stock_data(
        stock_code: str,  # 股票代码
        beg: str = '19000101',  # 开始日期，19000101，表示 1900年1月1日
        end: str = '20500101',  # 结束日期
        klt: int = 101,  # 行情之间的时间间隔 1、5、15、30、60分钟; 101:日; 102:周; 103:月
        fqt: int = 1,  # 复权方式，0 不复权 1 前复权 2 后复权
):
    try:
        qeury_url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get'
        callback = jquery_mock_callback()  # 没有cb这个参数也可以正确返回数据
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            # 模拟浏览器标识
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  # 可接受的内容类型
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',  # 语言偏好
            'Accept-Encoding': 'gzip, deflate, br',  # 支持的压缩格式
            'Connection': 'keep-alive',  # 保持长连接
            'Referer': 'https://quote.eastmoney.com/',  # 来源页面（用于反爬）
            'Content-Type': 'application/json',  # 请求体格式（POST/PUT时需设置）
            'Authorization': 'Bearer your_token_here',  # 身份验证（如JWT）
            'Cookie': 'session_id=abc123; user_pref=dark_mode'  # Cookie信息（需动态获取）
        }

        # 生成东方财富专用的secid
        if len(stock_code) == 5:
            secid = f'116.{stock_code}'  # 港股或其他特殊代码（需进一步验证）
        elif stock_code[:3] == '399':  # 深证指数（如399001深证成指）
            secid = f'0.{stock_code}'
        elif stock_code[:3] in ('000', '001', '002', '300'):  # 深市股票及中小创
            secid = f'0.{stock_code}'
        elif stock_code[:3] == '688':  # 沪市科创板
            secid = f'1.{stock_code}'
        elif stock_code[0] == '6':  # 沪市主板（60开头）及其他6开头代码
            secid = f'1.{stock_code}'
        else:  # 默认深市（如北交所转板等特殊情况需单独处理）
            secid = f'0.{stock_code}'
        print(secid)
        EASTMONEY_KLINE_FIELDS = {'f51': '日期', 'f52': '开盘', 'f53': '收盘', 'f54': '最高', 'f55': '最低',
                                  'f56': '成交量', 'f57': '成交额', 'f58': '振幅', 'f59': '涨跌幅', 'f60': '涨跌额',
                                  'f61': '换手率', }
        fields = list(EASTMONEY_KLINE_FIELDS.keys())
        # columns = list(EASTMONEY_KLINE_FIELDS.values())
        # fields1中:
        # f1=code=股票代码,f2=market=专用的secid,f3=name=股票名称,f4=decimal,f5=dktotal,f6=preKPrice,f7=prePrice,
        # f8=qtMiscType,f9,f10,f11,f12,f13=version
        fields2 = ",".join(fields)
        # ut:User Token 哈希值
        # 生成随机32位十六进制字符串
        random_token = secrets.token_hex(16)
        # 对特定数据生成哈希
        # data = "user123".encode()
        # hashed_token = hashlib.md5(data).hexdigest()
        # rtntype未知
        params = (
            ('cb', callback),
            ('secid', secid),
            ('ut', random_token),
            ('fields1', 'f1,f3'),
            ('fields2', fields2),
            ('beg', beg),
            ('end', end),
            ('rtntype', '6'),
            ('klt', f'{klt}'),
            ('fqt', f'{fqt}'),
        )
        json_response = requests.get(qeury_url, params=params, headers=headers, verify=False).text
        print(json_response)
    except Exception as e:
        print(f"股票 {stock_code} 数据获取失败: {str(e)}")
        return None
    return json_response


def process_stock(stock_code):
    """处理单个股票数据"""
    resp = get_stock_data(stock_code)
    # 检查 resp 是否为 None
    if resp is not None:
        json_start = resp.find('(')
    else:
        print("响应数据为 None，无法查找起始位置。")
        return None, None
    if json_start == -1:
        raise ValueError("无效的API响应格式")
    data_str = resp[json_start + 1:-2]  # +1跳过开头的(，-2去掉结尾的);
    # 检查 resp 是否为 None
    if resp is not None:
        try:
            json_data = json.loads(data_str)['data']
        except (json.JSONDecodeError, KeyError):
            print("解析JSON数据时出错，请检查响应数据格式。")
            return None, None
    else:
        print("响应数据为 None，无法解析。")
        return None, None
    stock_name = json_data['name']
    # 解析股票数据
    # 直接创建DataFrame
    klines = [kline.split(',') for kline in json_data['klines']]

    # 创建DataFrame时显式指定列类型
    df = pd.DataFrame(
        data=klines,
        columns=pd.Index([
            '日期', '开盘价', '收盘价', '最高价', '最低价',
            '成交量', '成交额', '成交幅', '涨跌幅', '涨跌额', '换手率'
        ], dtype='object')
    )

    # 新增：反转数据顺序（最新日期在前）
    df = df.iloc[::-1].reset_index(drop=True)

    # 格式化涨跌幅为百分比
    df['涨跌幅'] = df['涨跌幅'] + '%'

    return df, stock_name


if __name__ == "__main__":
    codes = input("请输入上市地区与股票代码（多个用逗号分隔）如:000001,300750:").split(',')

    retry_count = 3
    for i in range(retry_count):
        try:
            with pd.ExcelWriter('stock_detail.xlsx', engine='openpyxl') as writer:
                valid_sheets = 0
                for code in codes:
                    code = code.strip()
                    df, stock_name = process_stock(code)
                    if df is None or stock_name is None:
                        continue
                    # 生成合法的工作表名称
                    safe_sheet_name = f"{stock_name[:20]}({code})"[:31]
                    df.to_excel(writer, index=False, sheet_name=safe_sheet_name)

                    # 获取工作表对象时使用相同的名称
                    worksheet = writer.sheets[safe_sheet_name]

                    # 插入合并居中的标题行
                    worksheet.insert_rows(1)
                    title_cell = worksheet.cell(row=1, column=1, value=f"{stock_name}({code})")
                    title_cell.font = Font(bold=True)
                    title_cell.alignment = Alignment(horizontal='center', vertical='center')
                    worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=11)
                    valid_sheets += 1
                if valid_sheets == 0:  # 新增空文件检查
                    raise ValueError("所有股票数据获取失败，请检查代码和网络连接")
                print("所有股票数据保存成功！")
                break
        except PermissionError:
            if i < retry_count - 1:
                input(f"文件被占用，请关闭Excel后按回车重试（剩余尝试次数：{retry_count - i - 1}）")
            else:
                print("保存失败：多次尝试后文件仍被占用，请手动关闭Excel后重新运行程序")
                exit()
