# 456-main/V5_auto_grader/auto_grader.py

import json
from pathlib import Path

MODULE_PATH = Path("~/456-main/V1_core_generator/king_module.json").expanduser()
RESULT_PATH = Path("~/456-main/V2_market_simulator/simulated_result.json").expanduser()
OUTPUT_PATH = Path("~/456-main/V5_auto_grader/grading_result.json").expanduser()

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def score_module(result, king):
    trades = result.get("trades", [])
    if not trades:
        return {
            "score": 10,
            "grade": "D",
            "problem_flags": ["無交易", "模組無反應"],
            "evolution_suggestion": "檢查進場條件、降低延遲與提高進場敏感度"
        }

    win_rate = sum(1 for t in trades if t["pnl"] > 0) / len(trades)
    total_return = result["final_capital"] - king["capital"]
    avg_pnl = sum(t["pnl"] for t in trades) / len(trades)

    score = 50

    # 評分規則
    if total_return > 0:
        score += 20
    else:
        score -= 20

    if win_rate > 0.7:
        score += 15
    elif win_rate < 0.3:
        score -= 10

    if avg_pnl > 0:
        score += 10
    elif avg_pnl < -1:
        score -= 10

    # 等級評定
    grade = "S" if score >= 90 else "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D"

    # 問題標籤
    flags = []
    if win_rate < 0.3:
        flags.append("勝率過低")
    if avg_pnl < -1.5:
        flags.append("單筆虧損過大")
    if result["status"] == "dead":
        flags.append("爆倉")
    if score > 80 and total_return > 5:
        flags.append("表現優秀")

    # 建議
    if "爆倉" in flags:
        suggestion = "降低槓桿／減少進場倉位／提高停損敏感度"
    elif "勝率過低" in flags:
        suggestion = "嘗試調整 ma 參數，縮小進出判斷區間"
    elif "表現優秀" in flags:
        suggestion = "維持策略主幹，微幅強化進場條件"
    else:
        suggestion = "小幅隨機突變觀察效果"

    return {
        "score": round(score, 2),
        "grade": grade,
        "problem_flags": flags,
        "evolution_suggestion": suggestion
    }

def main():
    king = load_json(MODULE_PATH)
    result = load_json(RESULT_PATH)
    grading = score_module(result, king)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(grading, f, indent=2)

    print(f"[OK] 模組評分完成，分數：{grading['score']}，建議：{grading['evolution_suggestion']}")

if __name__ == "__main__":
    main()
