# 456-main/V1_core_generator/core_generator.py

import json
from datetime import datetime
from pathlib import Path

MODULE_ID = "king"
INIT_CAPITAL = 70.51
OUTPUT_PATH = Path("king_module.json")

king_module = {
    "id": MODULE_ID,
    "created_at": datetime.utcnow().isoformat(),
    "capital": INIT_CAPITAL,
    "strategy_type": "A",
    "parameters": {
        "ma_fast": 8,
        "ma_slow": 21,
        "sl_pct": 1.8,
        "tp_pct": 4.5
    },
    "style_profile": {
        "risk_tolerance": "medium",
        "emotional_tendency": "aggressive",
        "temperature_level": 0.7
    },
    "generation": 0,
    "live_rounds": 0,
    "performance": {
        "return_pct": 0.0,
        "sharpe": 0.0,
        "drawdown": 0.0,
        "win_rate": 0.0,
        "trade_count": 0
    }
}

with open(OUTPUT_PATH, "w") as f:
    json.dump(king_module, f, indent=2)

print(f"[OK] 模組 {MODULE_ID} 已建立，資金：{INIT_CAPITAL} USDT")
