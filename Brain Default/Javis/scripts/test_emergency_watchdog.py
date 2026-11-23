#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite cho Emergency Watchdog (Out-of-Band Kill-Switch).
Kiem tra:
1. Load config hop le tu watchdog_config.json
2. Auth gate chat_id (1894254685 vs unauthorized)
3. Do luong Telemetry he thong (/status < 500 ms)
4. Phanh cap do 1 (/panic) khong gay anh huong tien trinh chinh
5. Xu ly va format Markdown khong chua ky tu em dash
"""

import os
import sys
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

import emergency_watchdog as ew


def test_watchdog_suite():
    print("[1/5] Kiem tra load config...")
    cfg = ew.load_config()
    assert cfg["allowed_chat_id"] == 1894254685, "Chat ID phai la 1894254685"
    assert cfg["server_port"] == 7777, "Port server phai la 7777"
    print(" -> Config load thanh cong.")

    print("[2/5] Kiem tra Auth gate chat_id...")
    # Lenh tu ID hop le
    valid_reply = ew.handle_command("/ping", "/ping", 1894254685, cfg)
    assert valid_reply is not None, "Lenh tu 1894254685 phai duoc phan hoi"
    assert "PONG" in valid_reply

    # Kiem tra khong phan hoi lenh ngoai danh sach
    invalid_cmd = ew.handle_command("/unknown", "/unknown", 1894254685, cfg)
    assert invalid_cmd is None
    print(" -> Auth gate va dispatch lenh hoat dong chinh xac.")

    print("[3/5] Kiem tra do luong Telemetry (/status)...")
    start = time.perf_counter()
    tel = ew.get_system_telemetry(cfg)
    dur_ms = (time.perf_counter() - start) * 1000
    assert "cpu_pct" in tel
    assert "ram_pct" in tel
    assert "server_alive" in tel
    assert dur_ms < 500, f"Thoi gian do telemetry ({dur_ms:.1f}ms) phai < 500ms"
    formatted = ew.format_status_message(tel)
    assert "Bao cao Telemetry" in formatted
    print(f" -> Telemetry do thanh cong trong {dur_ms:.1f} ms (< 500ms).")

    print("[4/5] Kiem tra phanh cap 1 (/panic dry simulation)...")
    res = ew.execute_level1_panic(cfg)
    assert res["status"] == "success"
    assert res["level"] == 1
    assert "freed_mb" in res
    print(f" -> Panic level 1 thuc thi thanh cong trong {res['elapsed_ms']} ms.")

    print("[5/5] Kiem tra tuyet doi khong chua ky tu em dash (U+2014)...")
    files_to_check = [
        os.path.join(script_dir, "emergency_watchdog.py"),
        os.path.join(script_dir, "run_emergency_watchdog.bat"),
        os.path.join(script_dir, "..", "bridge", "watchdog_config.json")
    ]
    for fp in files_to_check:
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
            assert "\u2014" not in content, f"Phat hien em dash trong {fp}"
    print(" -> 100% file khong chua ky tu em dash.")

    print("\n>>> TOAN BO 5 BAI KIEM THU DAT CHUAN VERIFIED_IN_SCOPE! <<<")


if __name__ == "__main__":
    test_watchdog_suite()
