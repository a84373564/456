# 456-main/V6_memory_vault/memory_vault.py

import json
from pathlib import Path
from datetime import datetime

MODULE_PATH = Path("~/456-main/V1_core_generator/king_module.json").expanduser()
RESULT_PATH = Path("~/456-main/V2_market_simulator/simulated_result.json").expanduser()
GRADING_PATH = Path("~/456-main/V5_auto_grader/grading_result.json").expanduser()
MEMORY_PATH = Path("~/456-main/V6_memory_vault/king_memory.jsonl").expanduser()

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def append_memory(record):
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")

def record_memory():
    king = load_json(MODULE_PATH)
    result = load_json(RESULT_PATH)
    grade = load_json(GRADING_PATH)

    memory_record = {
        "timestamp": datetime.utcnow().isoformat(),
        "generation": king["generation"],
        "live_rounds": king["live_rounds"],
        "parameters": king["parameters"],
        "style_profile": king["style_profile"],
        "final_capital": result["final_capital"],
        "status": result["status"],
        "score": grade["score"],
        "grade": grade["grade"],
        "problem_flags": grade["problem_flags"],
        "evolution_suggestion": grade["evolution_suggestion"],
        "evolution_summary": king.get("evolution_summary", {})
    }

    append_memory(memory_record)
    print(f"[OK] å·²è¨éæ¨¡çµç¬¬ {king['live_rounds']} è¼ªè¨æ¶")

if __name__ == "__main__":
    record_memory()
