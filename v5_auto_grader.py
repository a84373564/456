# 456-main/V3_evolution_engine/evolution_engine.py

import json
import random
from pathlib import Path
from datetime import datetime

MODULE_PATH = Path("~/456-main/V1_core_generator/king_module.json").expanduser()
RESULT_PATH = Path("~/456-main/V2_market_simulator/simulated_result.json").expanduser()
GRADING_PATH = Path("~/456-main/V5_auto_grader/grading_result.json").expanduser()
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

def evolve_module(king, result, grading):
    outcome = result["final_capital"] - king["capital"]
    score = grading.get("score", 50)
    suggestion = grading.get("evolution_suggestion", "隨機調整")
    flags = grading.get("problem_flags", [])

    # 根據分數決定突變強度
    if score >= 80:
        scale = 0.03
    elif score >= 60:
        scale = 0.07
    elif score >= 40:
        scale = 0.12
    else:
        scale = 0.2

    # 根據情緒風格微調
    if king["style_profile"]["emotional_tendency"] == "aggressive":
        scale *= 1.2
    elif king["style_profile"]["emotional_tendency"] == "cautious":
        scale *= 0.8

    # 根據問題標籤自動進化偏向
    if "勝率過低" in flags:
        king["parameters"]["ma_fast"] = int(evolve_parameter(king["parameters"]["ma_fast"], scale, 1, 100))
        king["parameters"]["ma_slow"] = int(evolve_parameter(king["parameters"]["ma_slow"], scale, 2, 200))
    if "單筆虧損過大" in flags:
        king["parameters"]["sl_pct"] = evolve_parameter(king["parameters"]["sl_pct"], scale, 0.1, 10)
    if "爆倉" in flags:
        king["parameters"]["sl_pct"] = evolve_parameter(king["parameters"]["sl_pct"], scale * 1.5, 0.5, 10)
        king["style_profile"]["risk_tolerance"] = "low"
        king["style_profile"]["emotional_tendency"] = "cautious"
    if "表現優秀" in flags:
        scale *= 0.5  # 只做微幅調整

    # 總體進化參數
    king["parameters"]["tp_pct"] = evolve_parameter(king["parameters"]["tp_pct"], scale, 0.1, 20)

    # 累計進化歷程
    king["live_rounds"] += 1
    king["generation"] += 1

    # 演化摘要
    king["evolution_summary"] = {
        "timestamp": datetime.utcnow().isoformat(),
        "last_outcome": outcome,
        "score": score,
        "grade": grading.get("grade"),
        "problem_flags": flags,
        "mutation_strength": scale,
        "evolution_suggestion": suggestion,
        "adjusted_parameters": king["parameters"]
    }

    return king

def main():
    king = load_json(MODULE_PATH)
    result = load_json(RESULT_PATH)
    grading = load_json(GRADING_PATH)

    evolved = evolve_module(king, result, grading)
    save_json(OUTPUT_PATH, evolved)
    print(f"[OK] 模組進化完成，已讀取自評建議與分數，live_rounds：{evolved['live_rounds']}")

if __name__ == "__main__":
    main()
