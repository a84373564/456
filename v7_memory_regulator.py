# 456-main/V7_memory_regulator/memory_regulator.py

import json
from pathlib import Path
from hashlib import sha256

MEMORY_PATH = Path("~/456-main/V6_memory_vault/king_memory.jsonl").expanduser()
CLEANED_PATH = Path("~/456-main/V6_memory_vault/king_memory_cleaned.jsonl").expanduser()
DEDUPE_KEY_FIELDS = ["parameters", "score", "status", "generation"]

def compute_fingerprint(record):
    data = {k: record.get(k) for k in DEDUPE_KEY_FIELDS}
    key = json.dumps(data, sort_keys=True)
    return sha256(key.encode()).hexdigest()

def clean_memory():
    if not MEMORY_PATH.exists():
        print("[SKIP] 沒有記憶檔案，跳過清理")
        return

    fingerprints = set()
    cleaned = []

    with open(MEMORY_PATH, "r") as f:
        for line in f:
            record = json.loads(line.strip())
            fp = compute_fingerprint(record)
            if fp not in fingerprints:
                fingerprints.add(fp)
                cleaned.append(record)

    with open(CLEANED_PATH, "w") as f:
        for record in cleaned:
            f.write(json.dumps(record) + "\n")

    print(f"[OK] 記憶清理完成：原 {len(fingerprints)} 條有效紀錄已寫入 {CLEANED_PATH.name}")

if __name__ == "__main__":
    clean_memory()
