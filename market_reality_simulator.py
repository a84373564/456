# 456-main/V2_market_simulator/market_reality_simulator_max_v2.py

import requests
import json
import random
from pathlib import Path
from datetime import datetime

# === 檔案路徑設定 ===
MODULE_PATH = Path("~/456-main/V1_core_generator/king_module.json").expanduser()
CONFIG_PATH = Path("~/456-main/V2_market_simulator/sim_config.json").expanduser()
OUTPUT_PATH = Path("~/456-main/V2_market_simulator/simulated_result.json").expanduser()

# === 輔助函數 ===
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def fetch_kline(symbol, interval="1m", limit=300):
    url = "https://api.mexc.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json()

def apply_slippage(price, slippage_pct):
    return price * (1 + random.uniform(-slippage_pct, slippage_pct))

def should_fail_entry(fail_rate):
    return random.random() < fail_rate

# === 主模擬邏輯 ===
def simulate():
    king = load_json(MODULE_PATH)
    config = load_json(CONFIG_PATH)

    symbol = config.get("symbol", "DOGEUSDT")
    slippage_pct = config.get("slippage_pct", 0.001)
    delay_kline = config.get("delay_kline_count", 1)
    fee_pct = config.get("fee_pct", 0.001)
    fail_rate = config.get("entry_fail_rate", 0.05)
    max_loss_pct = config.get("max_loss_pct", 0.3)  # 倉控最大損失比例
    capital = king["capital"]
    tp_pct = king["parameters"]["tp_pct"] / 100
    sl_pct = king["parameters"]["sl_pct"] / 100

    klines = fetch_kline(symbol)
    trades = []
    position = None
    starting_capital = capital

    for i in range(delay_kline, len(klines)):
        open_time, open_price, high_price, low_price, close_price = int(klines[i][0]), float(klines[i][1]), float(klines[i][2]), float(klines[i][3]), float(klines[i][4])

        # 模擬行情切換（部分隨機波動加強）
        volatility_amp = random.uniform(0.8, 1.2)
        high_price *= volatility_amp
        low_price *= volatility_amp

        if position is None:
            if should_fail_entry(fail_rate):
                continue  # 假設滑單或委託失敗

            entry_price = apply_slippage(open_price, slippage_pct)
            risk_capital = capital * max_loss_pct
            position = {
                "entry_time": open_time,
                "entry_price": entry_price,
                "capital": risk_capital,
                "stop_loss": entry_price * (1 - sl_pct),
                "take_profit": entry_price * (1 + tp_pct)
            }
        else:
            if low_price <= position["stop_loss"]:
                exit_price = apply_slippage(position["stop_loss"], slippage_pct)
                result = "stop_loss"
            elif high_price >= position["take_profit"]:
                exit_price = apply_slippage(position["take_profit"], slippage_pct)
                result = "take_profit"
            else:
                continue

            gross_return = (exit_price - position["entry_price"]) / position["entry_price"]
            fee = fee_pct * 2
            net_return = gross_return - fee
            pnl = position["capital"] * net_return
            capital += pnl
            trades.append({
                "entry_time": position["entry_time"],
                "exit_time": open_time,
                "entry_price": position["entry_price"],
                "exit_price": exit_price,
                "result": result,
                "pnl": pnl,
                "capital": capital
            })
            position = None

        if capital <= 0:
            print("模組爆倉，資金歸零")
            break

    result = {
        "module_id": king["id"],
        "symbol": symbol,
        "final_capital": capital,
        "trade_count": len(trades),
        "trades": trades,
        "status": "dead" if capital <= 0 else "alive",
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[OK] 實戰模擬完成，結果寫入 {OUTPUT_PATH.name}")

if __name__ == "__main__":
    simulate()
