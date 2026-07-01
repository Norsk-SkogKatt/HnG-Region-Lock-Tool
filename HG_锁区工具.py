"""
HG 伺服器鎖區工具 v3.0
使用 ipinfo.io API 查詢伺服器 IP 地理位置
透過 Windows 進階防火牆 (netsh advfirewall) 建立雙向封鎖規則

靈感來自 HG 伺服器鎖定 v2.x 系列
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError

# ── 伺服器 IP 清單（合併舊版程式 + 實際 Ping 測試結果） ──
SERVERS: list[dict[str, str]] = [
    {"ip": "139.99.120.230", "region": "AS", "country": "SG-Singapore"},
    {"ip": "135.136.10.86", "region": "AS", "country": "HK-HongKong"},
    {"ip": "139.99.149.14", "region": "OC", "country": "AU-Sydney"},
    {"ip": "144.217.77.9", "region": "NA", "country": "CA-Quebec"},
    {"ip": "162.213.248.83", "region": "NA", "country": "US-Phoenix"},
    {"ip": "147.135.214.90", "region": "EU", "country": "FR-Dunkirk"},
    {"ip": "147.135.252.98", "region": "EU", "country": "FR-Dunkirk"},
    {"ip": "149.202.215.48", "region": "EU", "country": "FR-Dunkirk"},
    {"ip": "37.187.226.17", "region": "EU", "country": "FR-Dunkirk"},
    {"ip": "51.75.119.5", "region": "EU", "country": "FR-Dunkirk"},
    {"ip": "51.77.67.200", "region": "EU", "country": "DE-Frankfurt"},
    {"ip": "51.83.236.30", "region": "EU", "country": "PL-Warsaw"},
    {"ip": "51.91.74.237", "region": "EU", "country": "FR-Dunkirk"},
]

APP_NAMES: list[str] = ["hngsync", "HeroesAndGeneralsDesktop"]

REQUERY_DAYS = 7  # ipinfo.io 查詢快取天數

VALID_MODES: list[str] = ["AS-EU Only", "EU Only", "AS Only", "HK Only", "無"]

# ── 全域狀態 ──
LOG_FILE: str = ""
CONFIG_FILE: str = ""
app_paths: dict[str, str] = {}


# ═══════════════════════════════════════════════
# 工具函式
# ═══════════════════════════════════════════════

def _get_base_dir() -> str:
    """取得程式所在目錄（支援 PyInstaller 打包）"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def log_init() -> None:
    """初始化記錄檔"""
    global LOG_FILE
    base = _get_base_dir()
    LOG_FILE = os.path.join(base, "HG_lock.log")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"=== HG 鎖區工具 v3.0 - {datetime.now():%Y-%m-%d %H:%M:%S} ===\n")
        f.write(f"{'='*60}\n")


def log_raw(text: str) -> None:
    """寫入原始文字到記錄檔"""
    if not LOG_FILE:
        return
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except OSError:
        pass


def log_info(text: str) -> None:
    log_raw(f"[INFO] {text}")


def log_action(text: str) -> None:
    log_raw(f"[ACTION] {text}")


def log_error(text: str) -> None:
    log_raw(f"[ERROR] {text}")


# ═══════════════════════════════════════════════
# 設定檔管理
# ═══════════════════════════════════════════════

def _config_path() -> str:
    global CONFIG_FILE
    if not CONFIG_FILE:
        CONFIG_FILE = os.path.join(_get_base_dir(), "HG_config.json")
    return CONFIG_FILE


def load_config() -> dict:
    path = _config_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_config(hn_path: str = "", last_mode: str = "") -> None:
    cfg = load_config()
    if hn_path:
        cfg["hn_path"] = hn_path
    if last_mode:
        cfg["last_mode"] = last_mode
    cfg["last_updated"] = datetime.now().isoformat()
    try:
        with open(_config_path(), "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def _should_requery(cfg: dict) -> bool:
    """Check if 7 days have passed since last ipinfo query — if so, re-query."""
    last_time = cfg.get("last_query_time", "")
    if not last_time:
        return True
    try:
        last = datetime.fromisoformat(last_time)
        return (datetime.now() - last).days >= REQUERY_DAYS
    except (ValueError, TypeError):
        return True


def _cache_query_result(servers_info: list[dict]) -> None:
    """Save ipinfo query result + timestamp to config."""
    cfg = load_config()
    cfg["last_query_time"] = datetime.now().isoformat()
    cfg["cached_servers"] = servers_info
    try:
        with open(_config_path(), "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def _load_or_query_servers() -> list[dict]:
    """Load cached servers if <7 days old, otherwise query ipinfo.io."""
    cfg = load_config()
    if not _should_requery(cfg) and "cached_servers" in cfg:
        cached = cfg["cached_servers"]
        last_time = cfg.get("last_query_time", "?")[:10]
        print(f"\n[+] 使用快取 IP 資料（{last_time}，{REQUERY_DAYS} 天內有效）")
        print(f"    共 {len(cached)} 個伺服器")
        log_info(f"使用快取 IP 資料（查詢時間: {cfg.get('last_query_time', '?')}）")
        return cached
    # 需要重新查詢
    result = update_server_info()
    _cache_query_result(result)
    return result


# ═══════════════════════════════════════════════
# 管理員權限
# ═══════════════════════════════════════════════

def is_admin() -> bool:
    """檢查是否以管理員權限執行"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except (ImportError, AttributeError):
        return False


def run_as_admin() -> None:
    """以管理員權限重啟程式"""
    import ctypes
    script = sys.argv[0]
    params = " ".join(sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1
    )


# ═══════════════════════════════════════════════
# ipinfo.io IP 查詢
# ═══════════════════════════════════════════════

IPINFO_TOKEN = ""  # 可選：填入 ipinfo.io access token 以提升配額

def query_ipinfo(ip: str) -> Optional[dict]:
    """透過 ipinfo.io 查詢 IP 地理位置"""
    url = f"https://ipinfo.io/{ip}/json"
    if IPINFO_TOKEN:
        url += f"?token={IPINFO_TOKEN}"
    try:
        req = Request(url, headers={"User-Agent": "HG-Lock-Tool/3.0"})
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except URLError as e:
        log_error(f"IPInfo 查詢失敗 {ip}: {e}")
        return None
    except json.JSONDecodeError:
        log_error(f"IPInfo 回覆解析失敗 {ip}")
        return None


def update_server_info() -> list[dict]:
    """查詢所有伺服器 IP 的地理資訊，回傳更新後的清單"""
    print("\n[+] 正在透過 ipinfo.io 查詢伺服器位置...\n")
    updated = []
    total = len(SERVERS)
    for i, svr in enumerate(SERVERS, 1):
        ip = svr["ip"]
        print(f"  [{i}/{total}] {ip}... ", end="", flush=True)
        info = query_ipinfo(ip)
        if info:
            country = info.get("country", "")
            region = info.get("region", "")
            city = info.get("city", "")
            org = info.get("org", "")
            loc = info.get("loc", "")
            print(f"✓ {country} / {region} / {city}")
            log_info(f"{ip} -> {country}/{region}/{city} ({org})")
            updated.append({
                "ip": ip,
                "country": country,
                "region": region,
                "city": city,
                "org": org,
                "loc": loc,
            })
        else:
            # 查詢失敗則使用預設資料
            print(f"→ 使用預設 ({svr['country']})")
            log_info(f"{ip} 查詢失敗，使用預設: {svr['country']}")
            updated.append({**svr, "city": "", "org": "", "loc": ""})
        if i < total:
            time.sleep(0.3)  # 避免 API 限流
    return updated


# ═══════════════════════════════════════════════
# 防火牆操作（netsh advfirewall）
# ═══════════════════════════════════════════════

def run_netsh(args: list[str]) -> str:
    """執行 netsh 命令並回傳輸出"""
    cmd = ["netsh", "advfirewall", "firewall"] + args
    log_info(f"執行: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, capture_output=True, timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
        )
        stdout = result.stdout.decode("gbk", errors="replace") if result.stdout else ""
        stderr = result.stderr.decode("gbk", errors="replace") if result.stderr else ""
        output = stdout + stderr
        if result.returncode != 0:
            log_error(f"netsh 錯誤: {output.strip()}")
        return output.strip()
    except subprocess.TimeoutExpired:
        log_error("netsh 執行超時")
        return ""
    except FileNotFoundError:
        log_error("找不到 netsh.exe，請確認 Windows 防火牆可用")
        return ""


def get_rule_lines(keyword: str = "HG-") -> list[str]:
    """取得所有符合關鍵字的防火牆規則名稱"""
    output = run_netsh(["show", "rule", "name=all"])
    names: list[str] = []
    in_block = False
    for line in output.splitlines():
        stripped = line.strip()
        if keyword in stripped or ":" in stripped:
            if ":" not in stripped:
                continue
        if ":" not in stripped:
            continue
        parts = stripped.split(":", 1)
        if len(parts) == 2:
            name = parts[1].strip()
            if name and keyword in name:
                names.append(name)
    return names


def remove_old_rules() -> None:
    """移除舊版規則（v1/v2 格式）"""
    rules = get_rule_lines("HG-")
    if not rules:
        return
    print(f"\n[+] 發現 {len(rules)} 條舊規則，正在清除...")
    for name in rules:
        run_netsh(["delete", "rule", f'name={name}'])
        print(f"    已刪除: {name}")
    log_action(f"已清除 {len(rules)} 條舊規則")


def add_block_rules(
    ip: str, country: str, total: int = 0, current: int = 0
) -> int:
    """為指定 IP 在每個目標程式上建立雙向封鎖規則"""
    for app in APP_NAMES:
        name_in = f"HG-{ip}({country})-{app}-IN"
        name_out = f"HG-{ip}({country})-{app}-OUT"
        prog = app_paths.get(app, "")

        # 新增傳入規則
        args_in = [
            "add", "rule",
            f"name={name_in}",
            "dir=in",
            f"remoteip={ip}",
            "action=block",
            f"program={prog}",
            "protocol=any",
        ]
        run_netsh(args_in)
        current += 1
        if total:
            _show_progress(current, total, f"{ip}({country}) {app} IN")

        # 新增傳出規則
        args_out = [
            "add", "rule",
            f"name={name_out}",
            "dir=out",
            f"remoteip={ip}",
            "action=block",
            f"program={prog}",
            "protocol=any",
        ]
        run_netsh(args_out)
        current += 1
        if total:
            _show_progress(current, total, f"{ip}({country}) {app} OUT")

        log_action(f"已新增 {name_in} / {name_out}")
    return current


def _show_progress(current: int, total: int, label: str = "") -> None:
    """顯示進度條"""
    bar_width = 30
    filled = bar_width * current // total
    bar = "█" * filled + "░" * (bar_width - filled)
    pct = 100 * current // total
    print(f"\r    [{bar}] {pct:>3}%  {label}", end="", flush=True)
    if current >= total:
        print()


def remove_all_rules() -> int:
    """移除所有 HG 相關的防火牆規則"""
    rules = get_rule_lines("HG-")
    count = len(rules)
    if not rules:
        print("    無 HG 相關規則")
        return 0
    for i, name in enumerate(rules, 1):
        run_netsh(["delete", "rule", f'name={name}'])
        _show_progress(i, count, f"刪除: {name}")
    print(f"\n    已移除 {count} 條規則")
    log_action(f"已移除所有規則 ({count} 條)")
    return count


def show_current_rules() -> None:
    """顯示目前的 HG 防火牆規則"""
    rules = get_rule_lines("HG-")
    if rules:
        print(f"\n目前 HG 防火牆規則 ({len(rules)} 條):")
        for name in sorted(rules):
            print(f"  - {name}")
    else:
        print("\n目前無任何 HG 防火牆規則")


# ═══════════════════════════════════════════════
# 遊戲路徑選擇
# ═══════════════════════════════════════════════

def select_hn_root() -> str:
    """選擇 Heroes & Generals 遊戲安裝路徑"""
    cfg = load_config()
    saved = cfg.get("hn_path", "").replace("/", "\\")

    if saved and all(
        os.path.isfile(os.path.join(saved, f"{app}.exe"))
        for app in APP_NAMES
    ):
        print(f"[*] 自動使用上次路徑：{saved}")
        log_info(f"使用上次路徑: {saved}")
        return saved

    print("\n[?] 請指定 HnG 遊戲安裝路徑")
    path = ""
    while not path:
        raw = input("路徑: ").strip().strip("\"'").replace("/", "\\").rstrip("\\")
        path = raw
        if not path:
            print("[!] 路徑不得留空")
            continue

        missing = []
        for app in APP_NAMES:
            exe = os.path.join(path, f"{app}.exe")
            if not os.path.isfile(exe):
                missing.append(app)

        if missing:
            print("[!] 找不到以下檔案：")
            for m in missing:
                print(f"    - {m}.exe")
            print("    請確認路徑後再試。\n")
            retry = input("按 Enter 重試，或輸入 Q 離開: ").strip().upper()
            if retry == "Q":
                sys.exit(0)
            path = ""
        else:
            print("\n[✓] 已確認以下程式：")
            for app in APP_NAMES:
                print(f"    {app}.exe")
            log_info(f"遊戲路徑: {path}")
            save_config(hn_path=path, last_mode=cfg.get("last_mode", ""))
            return path

    return ""  # unreachable


# ═══════════════════════════════════════════════
# 封鎖邏輯
# ═══════════════════════════════════════════════

def invoke_block(label: str, filter_func) -> None:
    """執行封鎖操作

    Args:
        label: 操作名稱（用於顯示和記錄）
        filter_func: 過濾函式，接收 server dict，回傳 True 表示「此 IP 應被封鎖」
    """
    global app_paths
    print(f"\n[+] {label}...")

    # 清除舊規則
    remove_all_rules()
    time.sleep(0.5)

    # 過濾出要封鎖的 IP
    block_list = [x for x in servers_info if filter_func(x)]
    total = len(block_list) * len(APP_NAMES) * 2  # IN + OUT per app

    print(f"    共 {len(block_list)} 個 IP，將建立 {total} 條規則\n")

    current = 0
    for item in block_list:
        current = add_block_rules(
            item["ip"], item["country"], total, current
        )

    print()
    show_current_rules()
    print(f"\n[✓] {len(block_list)} 個 IP 已雙向封鎖（傳入 + 傳出）")
    log_action(f"{label}：{len(block_list)} 個 IP 已雙向封鎖")


# ═══════════════════════════════════════════════
# 介面
# ═══════════════════════════════════════════════

def write_banner() -> None:
    """顯示標題畫面"""
    os.system("cls")
    print("╔═══════════════════════════════════════════════╗")
    print("║       HG 伺服器鎖區工具 v3.0                  ║")
    print("║       雙向（傳入 + 傳出）封鎖 · ipinfo.io     ║")
    print("╚═══════════════════════════════════════════════╝")
    print("目標程式：hngsync.exe、HeroesAndGeneralsDesktop.exe")
    print("封鎖模式：傳入 / 傳出雙向封鎖，全協議，全埠")
    print()
    print("規則計算說明：")
    print("  每個 IP × 2 個程式 × 2 方向 = 每 IP 4 條規則")
    print()


def show_ip_distribution() -> None:
    """顯示 IP 分佈統計"""
    regions: dict[str, list[str]] = {}
    for svr in servers_info:
        r = svr.get("region", "??")
        if r not in regions:
            regions[r] = []
        regions[r].append(f"{svr['ip']} ({svr.get('country', '?')})")

    print("IP 分佈（ipinfo.io 查詢結果）：")
    region_labels = {
        "EU": "歐洲",
        "AS": "亞洲",
        "NA": "北美",
        "OC": "大洋洲",
    }
    for r in ["EU", "AS", "NA", "OC"]:
        if r in regions:
            label = region_labels.get(r, r)
            desc = "  ".join(regions[r][:3])
            if len(regions[r]) > 3:
                desc += f"  ...等 {len(regions[r])} 個"
            print(f"  {label}（{r}）  {desc}")
    print()


servers_info: list[dict] = []


# ═══════════════════════════════════════════════
# 主程式
# ═══════════════════════════════════════════════

def main() -> None:
    global servers_info, app_paths

    log_init()
    log_info("使用者授權管理員權限")

    # 檢查管理員權限
    if not is_admin():
        print("[!] 需要管理員權限，正在請求...")
        log_info("請求管理員權限")
        run_as_admin()
        return

    set_console_size()

    # 載入或查詢 IP 資訊（自動判斷 7 天快取）
    servers_info = _load_or_query_servers()
    print("\\n按 Enter 繼續...")
    input()

    # 選擇遊戲路徑
    hn_path = select_hn_root()
    app_paths = {
        app: os.path.join(hn_path, f"{app}.exe")
        for app in APP_NAMES
    }

    # 主選單迴圈
    while True:
        cfg = load_config()
        saved_mode = cfg.get("last_mode", "")
        if saved_mode not in VALID_MODES:
            saved_mode = ""

        write_banner()
        show_ip_distribution()

        # 顯示上次使用的模式
        print(f"  上次使用：{saved_mode}" if saved_mode else "  上次使用：—")
        print()

        print("操作：")
        print(f"  [1] AS-EU Only   只留亞洲 + 歐洲，封鎖北美 + 大洋洲")
        print("  [2] EU Only      封鎖歐洲以外所有 IP")
        print("  [2] EU Only      封鎖歐洲以外所有 IP")
        print("  [3] AS Only      封鎖亞洲以外所有 IP")
        print("  [4] HK Only      僅連接香港，封鎖其餘所有 IP")
        print("  [5] Clear        移除所有 HG 防火牆規則")
        print("  [6] 重新查詢     重新透過 ipinfo.io 查詢 IP 位置")
        print("  [7] 變更路徑     重新指定 HnG 資料夾")
        print("  [0] 離開")
        choice = input("\n請選擇 (0-7): ").strip()

        if choice == "1":
            invoke_block("僅連亞歐", lambda x: x.get("region") in ("NA", "OC"))
            save_config(hn_path, "AS-EU Only")
        elif choice == "2":
            invoke_block("僅連歐洲", lambda x: x.get("region") != "EU")
            save_config(hn_path, "EU Only")
        elif choice == "3":
            invoke_block("僅連亞洲", lambda x: x.get("region") != "AS")
            save_config(hn_path, "AS Only")
        elif choice == "4":
            hk_ip = next(
                (s["ip"] for s in servers_info if s.get("region") == "AS"
                 and "HK" in s.get("country", "").upper()),
                "135.136.10.86",
            )
            invoke_block("僅連香港", lambda x: x["ip"] != hk_ip)
            save_config(hn_path, "HK Only")
        elif choice == "5":
            print("\n[+] 正在移除防火牆規則...")
            remove_all_rules()
            print()
            show_current_rules()
            print("\n[✓] 完成")
            log_action("已執行 Clear，所有 HG 規則已清除")
            save_config(hn_path, "無")
        elif choice == "6":
            servers_info = update_server_info()
            print("\n按 Enter 繼續...")
            input()
        elif choice == "7":
            print()
            hn_path = select_hn_root()
            app_paths = {
                app: os.path.join(hn_path, f"{app}.exe")
                for app in APP_NAMES
            }
            print("[✓] 路徑已更新")
        elif choice == "0":
            print("\n[-] 再見")
            break
        else:
            print("\n[!] 無效選項")
            input("按 Enter 繼續...")


def set_console_size(cols: int = 90, lines: int = 40) -> None:
    """設定主控台視窗大小"""
    try:
        import ctypes
        from ctypes import wintypes

        ctypes.windll.kernel32.SetConsoleTitleW("HG 伺服器鎖區工具 v3.0")
        os.system(f"mode con cols={cols} lines={lines}")

        h = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        buf = wintypes._COORD(cols, 3000)
        ctypes.windll.kernel32.SetConsoleScreenBufferSize(h, buf)
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        print("\n[!] 發生未預期的錯誤，請截圖或記錄上方紅色文字。")
        print("    你也可以檢查 HG_lock.log 中的錯誤日誌。")
        print("\n按任意鍵離開...")
        try:
            import msvcrt
            msvcrt.getch()
        except ImportError:
            input()
