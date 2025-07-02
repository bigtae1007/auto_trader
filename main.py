# main.py

import logging
from trader.executor import run_trading_cycle

# 로그 설정
logging.basicConfig(
    filename="logs/auto_trader.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

print("✅ 코인 자동매매 프로그램 시작!")

if __name__ == "__main__":
    run_trading_cycle()