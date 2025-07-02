# trader/executor.py

import time
import logging
from config import settings
from trader.binance_api import create_binance_client, get_candle_data, place_order
from strategy.simple_ma import should_buy


def run_trading_cycle():
    client = create_binance_client()

    while True:
        try:
            candles = get_candle_data(
                client,
                symbol=settings.DEFAULT_SYMBOL,
                interval=settings.DEFAULT_INTERVAL,
                limit=5
            )

            for c in candles:
                print(f"🕒 시간: {c[0]} / 시가: {c[1]} / 종가: {c[4]}")

            if should_buy(candles):
                print("📈 [시그널] 매수 조건이 충족되었습니다!")
                logging.info("매수 조건 충족")

                # 주문 실행
                quantity = 0.001  # 테스트용 수량
                place_order(client, symbol=settings.DEFAULT_SYMBOL, quantity=quantity)
            else:
                print("📉 [시그널] 아직 매수 조건이 아닙니다.")

        except Exception as e:
            logging.error(f"❌ 오류 발생: {e}")
            print(f"❌ 예외 발생: {e}")

        # 30초 대기
        print("⏳ 다음 실행까지 30초 대기...\n")
        time.sleep(5)
