# backtester/backtest_runner.py

import csv
from strategy.simple_ma import should_buy, should_sell

BACK_TEST_PRICE = 1000000.0
# 초기값 세팅
usd_balance = BACK_TEST_PRICE
btc_balance = 0.0
is_holding = False

fee_rate = 0.001  # 0.1%

buy_count = 0
sell_count = 0
# 초기값 세팅 완료

# 테스트 코드 데이터 경로
file_path = "backtester/data/BTCUSDT_1m.csv"

# 캔들 데이터를 저장할 리스트
candles = []

# 파일을 열어서 데이터를 읽는다
with open(file_path, mode='r') as f:
    reader = csv.reader(f)
    next(reader)  # 첫 줄은 헤더니까 건너뛴다

    for row in reader:
        candles.append(row)

lookback = 100  # 전략 판단용 캔들 개수 제한

for i in range(lookback, len(candles)):
    window = candles[i - lookback:i]
    price = float(candles[i][4])  # 현재 시점 종가

    # 💸 자산 없으면 반복 중단
    if usd_balance < 1e-6 and btc_balance < 1e-6:
        print(f"\n💸 자산 소진 → 백테스트 중단 ({i}번째 캔들에서)")
        break

    # 매수 조건 판단
    if not is_holding and should_buy(window):
        # 전액 BTC 매수 (수수료 고려)
        btc_balance = (usd_balance / price) * (1 - fee_rate)
        usd_balance = 0.0
        is_holding = True
        buy_count += 1
        print(f"[매수] {i}번째 | 가격: {price:.2f} | BTC: {btc_balance:.6f}")

    # 매도 조건 판단
    elif is_holding and should_sell(window):
        # 전량 매도 (수수료 고려)
        usd_balance = (btc_balance * price) * (1 - fee_rate)
        btc_balance = 0.0
        is_holding = False
        sell_count += 1
        print(f"[매도] {i}번째 | 가격: {price:.2f} | USD: {usd_balance:.2f}")

# 백테스트 종료 후 평가
final_price = float(candles[-1][4])
total_asset = usd_balance + (btc_balance * final_price)
profit_percent = ((total_asset - 1000) / 1000) * 100


# HODL 수익률 계산
first_price = float(candles[lookback][4])  # 실제 매매 시작 시점 기준
last_price = final_price

btc_hodl = BACK_TEST_PRICE / first_price
usd_hodl = btc_hodl * last_price
hodl_profit_percent = ((usd_hodl - BACK_TEST_PRICE) / BACK_TEST_PRICE) * 100

print("\n=== 비교 결과 ===")
print(f"[매도 매수] 매수 횟수: {buy_count} | 매도 횟수: {sell_count}")
print(f"[전략 수익률] 최종 자산: ${total_asset:.2f} | 수익률: {profit_percent:.2f}%")
print(f"[단순 보유]   최종 자산: ${usd_hodl:.2f} | 수익률: {hodl_profit_percent:.2f}%")
