# 456-main/V4_insight_reporter/insight_reporter.py

import json
from pathlib import Path
from statistics import mean

MODULE_PATH = Path("~/456-main/V1_core_generator/king_module.json").expanduser()
RESULT_PATH = Path("~/456-main/V2_market_simulator/simulated_result.json").expanduser()
OUTPUT_PATH = Path("~/456-main/V4_insight_reporter/report_v4.txt").expanduser()

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def analyze_trades(trades):
    pnl_list = [t["pnl"] for t in trades]
    win_trades = [p for p in pnl_list if p > 0]
    loss_trades = [p for p in pnl_list if p <= 0]
    total = len(pnl_list)

    return {
        "total_trades": total,
        "win_rate": round(len(win_trades) / total * 100, 2) if total > 0 else 0.0,
        "avg_win": round(mean(win_trades), 4) if win_trades else 0.0,
        "avg_loss": round(mean(loss_trades), 4) if loss_trades else 0.0,
        "max_loss": round(min(pnl_list), 4) if pnl_list else 0.0,
        "max_gain": round(max(pnl_list), 4) if pnl_list else 0.0
    }

def classify_behavior(analysis, result, king):
    if result["status"] == "dead":
        return "çåå"
    if analysis["win_rate"] > 80 and analysis["avg_win"] > abs(analysis["avg_loss"]):
        return "ç©©å¥å"
    if analysis["win_rate"] < 40 and analysis["avg_loss"] < -king["capital"] * 0.1:
        return "èºé²å"
    return "ä¸­æ§å"

def generate_report():
    king = load_json(MODULE_PATH)
    result = load_json(RESULT_PATH)
    trades = result.get("trades", [])
    analysis = analyze_trades(trades)
    behavior = classify_behavior(analysis, result, king)

    report = []
    report.append(f"[æ¨¡çµ ID] {king['id']}")
    report.append(f"[é¢¨æ ¼] {king['style_profile']}")
    report.append(f"[ç­ç¥åæ¸] {king['parameters']}")
    report.append(f"[æ¨¡æ¬çµæ] è³é {king['capital']} â {result['final_capital']}ï¼çæï¼{result['status']}")
    report.append(f"[äº¤æçµ±è¨] ç¸½äº¤ææ¸ï¼{analysis['total_trades']}, åçï¼{analysis['win_rate']}%")
    report.append(f" - å¹³åç²å©ï¼{analysis['avg_win']}, å¹³åè§æï¼{analysis['avg_loss']}")
    report.append(f" - æå¤§ç²å©ï¼{analysis['max_gain']}, æå¤§è§æï¼{analysis['max_loss']}")
    report.append(f"[æ¨¡çµè¡çºé¡å] {behavior}")
    report.append(f"[è¼ªæ¬¡] live_rounds: {king['live_rounds']}, generation: {king['generation']}")
    report.append(f"[æ¼åæè¦] {king.get('evolution_summary', {})}")

    with open(OUTPUT_PATH, "w") as f:
        f.write("\n".join(report))

    print(f"[OK] å·²è¼¸åºæ¨¡çµå ±åè³ï¼{OUTPUT_PATH.name}")

if __name__ == "__main__":
    generate_report()
