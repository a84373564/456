# 456-main/autopilot_launcher.py

import subprocess
import time
from pathlib import Path

MODULES = [
    ("V1_core_generator/core_generator.py", "初始化模組（V1）"),
    ("V2_market_simulator/market_reality_simulator.py", "模擬市場（V2）"),
    ("V5_auto_grader/auto_grader.py", "自我評分（V5）"),
    ("V3_evolution_engine/evolution_engine.py", "模組進化（V3）"),
    ("V6_memory_vault/memory_vault.py", "記憶錄入（V6）"),
    ("V4_insight_reporter/insight_reporter.py", "產出報告（V4）"),
    ("V7_memory_regulator/memory_regulator.py", "記憶清理（V7）")
]

def run_script(script_path, label):
    full_path = Path("~/456-main").expanduser() / script_path
    print(f"[RUN] {label} → {script_path}")
    start = time.time()
    subprocess.run(["python3", str(full_path)], check=True)
    end = time.time()
    print(f"[OK] {label} 完成，用時 {round(end - start, 2)} 秒\n")

def main():
    total_start = time.time()
    for path, label in MODULES:
        run_script(path, label)
    total_end = time.time()
    print(f"=== 本輪執行完成，總耗時 {round(total_end - total_start, 2)} 秒 ===")

if __name__ == "__main__":
    main()
