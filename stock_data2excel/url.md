```
push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery3510012524248926530257_1742883047971&secid=116.01810&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=1&end=20500101&lmt=120&_=1742883047982
```

```
push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg=0&end=20500101&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6&secid=0.300750&klt=101&fqt=1&end=20500101&lmt=120&cb=jsonp1742888471585
```

```
push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery35107655400188973199_1742958006164&secid=116.01810&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=1&beg=0&end=20500101&smplmt=1202.33&lmt=1000000&_=1742893381976
```

```
push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery35104018603901715345_1742893381970&secid=116.01810&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=1&beg=0&end=20500101&smplmt=1202.33&lmt=1000000&_=1742893381976
```



```python
# cb = callback 

def jquery_mock_callback():
    jQuery_Version = "3.5.1"
    timestamp = int(round(time.time() * 1000))
    return "jQuery" + (jQuery_Version + str(random.random())).replace(".", "") + "_" + str(
        timestamp - 1000)
```









```
push2his.eastmoney.com/api/qt/stock/kline/get?
cb=jQuery35105377830202283694_1742974087647&
ut=fa5fd1943c7b386f172d6893dbfba10b&
secid=116.01810&
fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&
fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&
beg=20241101&
end=20500101&
rtntype=6&
klt=101&
fqt=1&

```

```
f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61
```

```
        stock_codes: str,  # 股票代码
        beg: str = '20241101',  # 开始日期，19000101，表示 1900年1月1日
        end: str = '20500101',  # 结束日期
        klt: int = 101,  # 行情之间的时间间隔 1、5、15、30、60分钟; 101:日; 102:周; 103:月
        fqt: int = 1,  # 复权方式，0 不复权 1 前复权 2 后复权
```

