# trader/binance_api.py

from binance.client import Client
from config import settings

import logging
def create_binance_client():
    client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET_KEY)
    return client


def get_candle_data(client, symbol="BTCUSDT", interval="1m", limit=10):
    """
    바이낸스에서 캔들(봉) 데이터를 받아옴
    :param client: Binance Client 객체
    :param symbol: 코인 심볼 (ex. BTCUSDT)
    :param interval: 시간 간격 (ex. 1m, 5m, 1h)
    :param limit: 몇 개 받아올지
    :return: 캔들 리스트
    """
    candles = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    return candles

# trader/binance_api.py (추가)

def place_order(client, symbol, quantity):
    """
    매수 주문 실행 함수 (현실에서는 POST 요청)
    여기서는 실제 주문은 하지 않고 로그만 출력
    """
    # 👉 실 주문하려면 아래 주석 해제
    # order = client.order_market_buy(
    #     symbol=symbol,
    #     quantity=quantity
    # )
    # return order

    # 📦 시뮬레이션 로그 출력
    print(f"🚀 [가상 주문] {symbol} 코인을 {quantity}개 매수합니다!")
    logging.info(f"[가상 주문] {symbol} 코인을 {quantity}개 매수!")
    return {"status": "success", "symbol": symbol, "quantity": quantity}