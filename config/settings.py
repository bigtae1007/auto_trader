# config/settings.py

import os
from dotenv import load_dotenv

# 1. 환경명 가져오기 (운영체제 환경변수 or 기본값)
ENV = os.getenv("ENV", "dev")

# 2. env 파일 경로 설정
env_file = f".env.{ENV}"

# 3. 해당 파일 로딩
load_dotenv(dotenv_path=env_file)

RUN_MODE = os.getenv("RUN_MODE", "development")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# 거래 기본 설정
DEFAULT_SYMBOL = "BTCUSDT"  # 기본 거래 코인
DEFAULT_INTERVAL = "1m"     # 캔들 간격 (1분봉)