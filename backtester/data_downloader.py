# data_downloader.py

import os
import csv
import time
from datetime import datetime, timedelta
from binance.client import Client
from config import settings

client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET_KEY)

def fetch_and_save_klines(symbol, interval, start_str, end_str, file_path):
    print(f"📥 {symbol} 데이터 다운로드 시작")

    # CSV 파일 오픈
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])

        start_ts = int(datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
        end_ts = int(datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)

        while start_ts < end_ts:
            try:
                candles = client.get_klines(
                    symbol=symbol,
                    interval=interval,
                    startTime=start_ts,
                    endTime=end_ts,
                    limit=1000
                )
                if not candles:
                    print("⚠️ 더 이상 데이터 없음")
                    break

                writer.writerows(candles)

                # 다음 시작 시간은 마지막 캔들의 closeTime + 1ms
                start_ts = candles[-1][6] + 1

                print(f"  - 진행 중... 현재 시간: {datetime.fromtimestamp(start_ts / 1000)}")

                # 요청 제한 방지를 위한 대기
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ 에러 발생: {e}")
                time.sleep(2)

    print(f"✅ {symbol} 데이터 저장 완료 → {file_path}")

def download_all():
    os.makedirs("data", exist_ok=True)
    # 테스트 항목들
    # "BTCUSDT", "ETHUSDT", "XRPUSDT"
    symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]
    interval = "1m"
    start = "2021-05-05 00:00:00"
    end   = "2025-05-05 00:00:00"

    for symbol in symbols:
        filename = f"data/{symbol}_{interval}.csv"
        fetch_and_save_klines(symbol, interval, start, end, filename)

if __name__ == "__main__":
    download_all()