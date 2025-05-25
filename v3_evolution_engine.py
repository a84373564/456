# 456-main/V3_evolution_engine/evolution_engine.py

import json
import random
from pathlib import Path
from datetime import datetime

MODULE_PATH = Path("~/456-main/V1_core_generator/king_module.json").expanduser()
RESULT_PATH = Path("~/456-main/V2_market_simulator/simulated_result.json").expanduser()
OUTPUT_PATH = MODULE_PATH  # 直接覆寫 king_module.json

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def bounded(x, min_val, max_val):
    return max(min_val, min(x, max_val))

def evolve_parameter(value, scale=0.1, minimum=0.01, maximum=100):
    mutation = value * random.uniform(-scale, scale)
    return round(bounded(value + mutation, minimum, maximum), 4)

def evolve_module(king, result):
    performance = result.get("final_capital", king["capital"])
    initial_capital = king["capital"]
    outcome = performance - initial_capital

    # 基本突變強度調整
    strong_mutation = outcome < 0  # 若虧損 → 強突變
    scale = 0.2 if strong_mutation else 0.05

    # 根據人格微調傾向
    if king["style_profile"]["emotional_tendency"] == "aggressive":
        scale *= 1.3
    elif king["style_profile"]["emotional_tendency"] == "cautious":
        scale *= 0.7

    # 進化參數
    king["parameters"]["ma_fast"] = int(evolve_parameter(king["parameters"]["ma_fast"], scale, 1, 100))
    king["parameters"]["ma_slow"] = int(evolve_parameter(king["parameters"]["ma_slow"], scale, 2, 200))
    king["parameters"]["sl_pct"] = evolve_parameter(king["parameters"]["sl_pct"], scale, 0.1, 10)
    king["parameters"]["tp_pct"] = evolve_parameter(king["parameters"]["tp_pct"], scale, 0.1, 20)

    # 累計進化輪次
    king["live_rounds"] += 1
    king["generation"] += 1

    # 記錄進化歷程摘要
    king["evolution_summary"] = {
        "timestamp": datetime.utcnow().isoformat(),
        "last_outcome": outcome,
        "mutation_strength": scale,
        "adjusted_parameters": king["parameters"]
    }

    return king

def main():
    king = load_json(MODULE_PATH)
    result = load_json(RESULT_PATH)

    evolved = evolve_module(king, result)
    save_json(OUTPUT_PATH, evolved)
    print(f"[OK] 模組已根據模擬結果完成進化，當前輪次：{evolved['live_rounds']}")

if __name__ == "__main__":
    main()
