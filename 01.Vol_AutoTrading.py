import time
import pyupbit
import datetime

access = "jD1JmAPdxciFn5gASRL6gyBTGvx6vXxNSrAGyEKx"
secret = "YuVFdltfkORufs35hFZt7JyS05aIgHbVD3Fm6KoN"

tickers = pyupbit.get_tickers(fiat="KRW")
print(tickers)

def get_min3_vol(ticker):
    """현재 3분봉 거래량 조회"""    
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=2)
    min3_vol = df['volume'].iloc[-1]
    return min3_vol

def get_pre_min3_vol(ticker):
    """직전 3분봉 거래량 조회"""    
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=3)
    pre_min3_vol = df['volume'].iloc[-2]    
    return pre_min3_vol

def get_pre_pre_min3_vol(ticker):
    """2직전 3분봉 거래량 조회"""    
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=4)
    pre_pre_min3_vol = df['volume'].iloc[-3]
    return pre_pre_min3_vol

def get_volxprice(ticker):
    """현재 3분봉 거래대금 조회"""    
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=2)
    volxprice = df['volume'].iloc[-1] * df['open'].iloc[-1]
    return volxprice

def get_ma10_price(ticker):
    """10.10분 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=11)
    ma10_price = df['close'].rolling(10).mean().iloc[-1]
    return ma10_price

def get_open_price(ticker):
    """3분봉 시작가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=2)
    open_price = df['volume'].iloc[-1]
    return open_price

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


while True:
    try:        
        for ticker in tickers:  
            pre_min3_vol = get_pre_min3_vol(ticker)     
            pre_pre_min3_vol = get_pre_pre_min3_vol(ticker)     
            min3_vol = get_min3_vol(ticker)
            ma10_price = get_ma10_price(ticker)
            current_price = pyupbit.get_current_price(ticker)
            volxprice = get_volxprice(ticker)
            open_price = get_open_price(ticker)
            balance = upbit.get_balance(ticker)
            now = datetime.datetime.now()
            print(ticker)
            print(balance)
            if (pre_min3_vol * 3 < min3_vol) and (pre_pre_min3_vol * 3 < min3_vol) and (ma10_price < current_price) and (balance < 0.000001) and (volxprice > 2000000000) and (open_price > 200): # 직전 거래량의 n배
                upbit.buy_market_order(ticker, 10000)
                buy_time = datetime.datetime.now()
                globals()[str(ticker) + 'sell_time_1'] = buy_time + datetime.timedelta(minutes=1)
                globals()[str(ticker) + 'sell_time_2'] = buy_time + datetime.timedelta(minutes=3)
                globals()[str(ticker) + 'sell_time_3'] = buy_time + datetime.timedelta(minutes=5)
                print(ticker) + print(current_price)
                
                # 매도시간을 어떻게..
                if globals()[str(ticker) + 'sell_time_1'] < now < globals()[str(ticker) + 'sell_time_1'] + datetime.timedelta(minutes=1):
                    balance = upbit.get_balance(ticker)
                    upbit.sell_market_order(ticker, balance*0.5)
                    print("sell1")
                elif globals()[str(ticker) + 'sell_time_2'] < now < globals()[str(ticker) + 'sell_time_2'] + datetime.timedelta(minutes=1):
                    balance = upbit.get_balance(ticker)
                    upbit.sell_market_order(ticker, balance*0.6)
                    print("sell2")
                elif globals()[str(ticker) + 'sell_time_3'] < now < globals()[str(ticker) + 'sell_time_3'] + datetime.timedelta(minutes=1):
                    balance = upbit.get_balance(ticker)
                    upbit.sell_market_order(ticker, balance*0.9995)
                    print("sell3")                
                else:
                    pass            
                # 매도시간을 어떻게..

            else:
                print("else")
            time.sleep(0.05)
    except Exception as e:
        print(e)
        time.sleep(1)

