import time
import pyupbit
import datetime

access = "access"
secret = "secret"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[1]['open'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

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

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=20):
            
            target_price_B = get_target_price("KRW-BTC", 0.84)            
            current_price_B = get_current_price("KRW-BTC")
            gap_B = target_price_B - current_price_B
            print("BTC_gap : " + str(gap_B))

            target_price_E = get_target_price("KRW-ETH", 0.73)
            current_price_E = get_current_price("KRW-ETH")
            gap_E = target_price_E - current_price_E
            print("ETH_gap : " + str(gap_E))

            if target_price_B < current_price_B:
                krw = get_balance("KRW")
                btc = get_balance("BTC")
                eth = get_balance("ETH")
                print("1")
                if btc < 0.01 :
                    upbit.buy_market_order("KRW-BTC", krw*0.5)
                    print("2")
                    if eth > 0.13 :
                        upbit.buy_market_order("KRW-BTC", krw*0.9995)
                        print("3")
                else:
                    print("4")
                    pass
            else:
                print("5")
                pass
            if target_price_E < current_price_E:
                krw = get_balance("KRW")
                btc = get_balance("BTC")
                eth = get_balance("ETH")
                print("6")
                if eth < 0.13 :
                    upbit.buy_market_order("KRW-ETH", krw*0.5)
                    print("7")
                    if btc > 0.01 :
                        upbit.buy_market_order("KRW-ETH", krw*0.9995)
                        print("8")
                else:
                    print("9")
                    pass
            else:
                print("10")
                pass
        else:
            btc = get_balance("BTC")
            eth = get_balance("ETH")
            print("11")
            if (btc > 0.0001) or (eth > 0.0013):
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                upbit.sell_market_order("KRW-ETH", eth*0.9995)
                print("12")
        print("13")
        time.sleep(0.5)
    except Exception as e:
        print(e)
        print("14")
        time.sleep(1)