"""
HG 伺服器鎖區工具 v4.0 (GUI)
使用 ipinfo.io API 查詢伺服器 IP 地理位置
透過 Windows 進階防火牆 (netsh advfirewall) 建立雙向封鎖規則
GUI 介面：大按鈕操作，靜默執行，一鍵開啟防火牆檢查
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.error import URLError
from urllib.request import Request, urlopen

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ── 伺服器 IP 清單 ──
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
    {"ip": "64.42.180.154", "region": "NA", "country": "US-Atlanta"},
]

APP_NAMES: list[str] = ["hngsync", "HeroesAndGeneralsDesktop"]
REQUERY_DAYS = 7  # ipinfo.io 查詢快取天數
IPINFO_TOKEN: str = ""

VALID_MODES: list[str] = ["AS-EU Only", "EU Only", "AS Only", "HK Only", "SG+EU Only", "無"]


# ═══════════════════════════════════════════════
# 工具函式（與 CLI 版共用）
# ═══════════════════════════════════════════════

def _get_base_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


LOG_FILE: str = ""
CONFIG_FILE: str = ""


def _log_path() -> str:
    global LOG_FILE
    if not LOG_FILE:
        LOG_FILE = os.path.join(_get_base_dir(), "HG_lock.log")
    return LOG_FILE


def _config_path() -> str:
    global CONFIG_FILE
    if not CONFIG_FILE:
        CONFIG_FILE = os.path.join(_get_base_dir(), "HG_config.json")
    return CONFIG_FILE


def log_raw(text: str) -> None:
    try:
        with open(_log_path(), "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except OSError:
        pass


def log_info(text: str) -> None:
    log_raw(f"[INFO] {text}")


def log_action(text: str) -> None:
    log_raw(f"[ACTION] {text}")


def log_error(text: str) -> None:
    log_raw(f"[ERROR] {text}")


def load_config() -> dict:
    try:
        with open(_config_path(), "r", encoding="utf-8") as f:
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
    """Check if 7 days have passed since last ipinfo query."""
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


def is_admin() -> bool:
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except (ImportError, AttributeError):
        return False


def run_as_admin() -> None:
    import ctypes
    script = sys.argv[0]
    params = " ".join(f'"{a}"' if " " in a else a for a in sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1
    )


# ── IP 查詢 ──

def query_ipinfo(ip: str) -> Optional[dict]:
    url = f"https://ipinfo.io/{ip}/json"
    if IPINFO_TOKEN:
        url += f"?token={IPINFO_TOKEN}"
    try:
        req = Request(url, headers={"User-Agent": "HG-Lock-Tool/4.0"})
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except (URLError, json.JSONDecodeError, OSError):
        return None


# ── 防火牆操作 ──

def run_netsh(args: list[str]) -> str:
    cmd = ["netsh", "advfirewall", "firewall"] + args
    log_info(f"執行: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, capture_output=True, timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
        )
        stdout = result.stdout.decode("gbk", errors="replace") if result.stdout else ""
        stderr = result.stderr.decode("gbk", errors="replace") if result.stderr else ""
        if result.returncode != 0:
            log_error(f"netsh 錯誤: {(stdout + stderr).strip()}")
        return (stdout + stderr).strip()
    except subprocess.TimeoutExpired:
        log_error("netsh 執行超時")
        return ""
    except FileNotFoundError:
        log_error("找不到 netsh.exe")
        return ""


def get_rule_lines(keyword: str = "HG-") -> list[str]:
    output = run_netsh(["show", "rule", "name=all"])
    names: list[str] = []
    for line in output.splitlines():
        if ":" not in line:
            continue
        parts = line.strip().split(":", 1)
        if len(parts) == 2:
            name = parts[1].strip()
            if name and keyword in name:
                names.append(name)
    return names


def remove_all_rules_silent() -> int:
    rules = get_rule_lines("HG-")
    count = len(rules)
    for name in rules:
        run_netsh(["delete", "rule", f'name={name}'])
    if count:
        log_action(f"已移除所有規則 ({count} 條)")
    return count


def add_block_rules_silent(ip: str, country: str) -> int:
    """為指定 IP 建立雙向封鎖規則，回傳新增規則數"""
    added = 0
    for app in APP_NAMES:
        prog = app_paths_global.get(app, "")
        name_in = f"HG-{ip}({country})-{app}-IN"
        name_out = f"HG-{ip}({country})-{app}-OUT"
        run_netsh([
            "add", "rule", f"name={name_in}", "dir=in",
            f"remoteip={ip}", "action=block",
            f"program={prog}", "protocol=any",
        ])
        added += 1
        run_netsh([
            "add", "rule", f"name={name_out}", "dir=out",
            f"remoteip={ip}", "action=block",
            f"program={prog}", "protocol=any",
        ])
        added += 1
        log_action(f"已新增 {name_in} / {name_out}")
    return added


# ── 全域狀態 ──

app_paths_global: dict[str, str] = {}


# ═══════════════════════════════════════════════
# GUI 應用程式
# ═══════════════════════════════════════════════

class HGLockerGUI:
    """HG 伺服器鎖區工具 GUI 版"""

    MODE_NAMES = {
        1: "AS-EU Only",
        2: "EU Only",
        3: "AS Only",
        4: "HK Only",
        5: "SG+EU Only",
    }

    REGION_LABELS = {"EU": "歐洲", "AS": "亞洲", "NA": "北美", "OC": "大洋洲"}

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("HG 伺服器鎖區工具 v4.0")
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap(default=os.path.join(_get_base_dir(), "icon.ico"))
        except Exception:
            pass

        self.servers_info: list[dict] = []
        self.hn_path: str = ""
        self.is_busy: bool = False  # 鎖定按鈕防止重複操作

        self._build_ui()
        self._init_session()

    # ─── UI 構建 ───

    def _build_ui(self) -> None:
        self.root.configure(bg="#f0f0f0")

        main = ttk.Frame(self.root, padding=16)
        main.pack(fill=tk.BOTH, expand=True)

        # 標題
        title = tk.Label(main, text="HG 伺服器鎖區工具", font=("Segoe UI", 18, "bold"),
                         bg="#f0f0f0", fg="#1a1a2e")
        title.pack(pady=(0, 4))

        subtitle = tk.Label(main, text="雙向封鎖 · ipinfo.io 自動查詢", font=("Segoe UI", 9),
                            bg="#f0f0f0", fg="#666")
        subtitle.pack(pady=(0, 12))

        # ── IP 分佈顯示 ──
        self.ip_frame = ttk.LabelFrame(main, text="伺服器 IP 分佈", padding=8)
        self.ip_frame.pack(fill=tk.X, pady=(0, 12))
        self.ip_labels: dict[str, tk.Label] = {}
        ip_inner = ttk.Frame(self.ip_frame)
        ip_inner.pack(fill=tk.X)
        for r in ("AS", "EU", "NA", "OC"):
            row = ttk.Frame(ip_inner)
            row.pack(fill=tk.X, pady=1)
            tag = tk.Label(row, text=f"  {self.REGION_LABELS.get(r, r)} ({r}):",
                           font=("Segoe UI", 9), anchor="w", bg="#f9f9f9")
            tag.pack(side=tk.LEFT)
            val = tk.Label(row, text="查詢中...", font=("Segoe UI", 9),
                           anchor="w", bg="#f9f9f9", fg="#888")
            val.pack(side=tk.LEFT, padx=(6, 0))
            self.ip_labels[r] = val

        # ── 模式按鈕（2×2 網格） ──
        btn_frame = ttk.Frame(main)
        btn_frame.pack(pady=(0, 8))

        btn_style = {"font": ("Segoe UI", 13, "bold"), "width": 14}

        self.btn_1 = tk.Button(btn_frame, text="① AS-EU Only\n只留亞洲+歐洲", **btn_style,
                               command=lambda: self._on_mode(1))
        self.btn_1.grid(row=0, column=0, padx=5, pady=4)

        self.btn_2 = tk.Button(btn_frame, text="② EU Only\n只留歐洲", **btn_style,
                               command=lambda: self._on_mode(2))
        self.btn_2.grid(row=0, column=1, padx=5, pady=4)

        self.btn_3 = tk.Button(btn_frame, text="③ AS Only\n只留亞洲", **btn_style,
                               command=lambda: self._on_mode(3))
        self.btn_3.grid(row=1, column=0, padx=5, pady=4)

        self.btn_4 = tk.Button(btn_frame, text="④ HK Only\n只留香港", **btn_style,
                               command=lambda: self._on_mode(4))
        self.btn_4.grid(row=1, column=1, padx=5, pady=4)

        self.btn_5 = tk.Button(btn_frame, text="⑤ SG+EU Only\n只留星洲+歐洲", **btn_style,
                               command=lambda: self._on_mode(5))
        self.btn_5.grid(row=2, column=0, columnspan=2, padx=5, pady=4, sticky="ew")

        # ── 清除按鈕 ──
        self.btn_clear = tk.Button(main, text="⑥ 清除所有規則 Clear", font=("Segoe UI", 11, "bold"),
                                   command=self._on_clear,
                                   width=35, height=2)
        self.btn_clear.pack(pady=(0, 10))

        # ── 分隔線 ──
        sep = ttk.Separator(main, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=(0, 8))

        # ── 狀態列 ──
        status_frame = ttk.Frame(main)
        status_frame.pack(fill=tk.X, pady=(0, 8))

        self.lbl_mode = tk.Label(status_frame, text="目前模式: —", font=("Segoe UI", 10),
                                 anchor="w", bg="#f0f0f0")
        self.lbl_mode.pack(fill=tk.X)

        self.lbl_path = tk.Label(status_frame, text="遊戲路徑: 尚未設定", font=("Segoe UI", 10),
                                 anchor="w", bg="#f0f0f0")
        self.lbl_path.pack(fill=tk.X)

        self.lbl_busy = tk.Label(status_frame, text="", font=("Segoe UI", 10),
                                 anchor="w", bg="#f0f0f0", fg="#e07c24")
        self.lbl_busy.pack(fill=tk.X)

        # ── 底部按鈕列 ──
        bottom = ttk.Frame(main)
        bottom.pack(fill=tk.X)

        self.btn_fw = tk.Button(bottom, text="🛡 開啟防火牆", font=("Segoe UI", 10),
                                command=self._open_firewall,
                                padx=8, pady=4)
        self.btn_fw.pack(side=tk.LEFT, padx=(0, 4))

        self.btn_requery = tk.Button(bottom, text="🔄 重新查詢", font=("Segoe UI", 10),
                                     command=self._on_requery,
                                     padx=8, pady=4)
        self.btn_requery.pack(side=tk.LEFT, padx=4)

        self.btn_path = tk.Button(bottom, text="📁 變更路徑", font=("Segoe UI", 10),
                                  command=self._on_change_path,
                                  padx=8, pady=4)
        self.btn_path.pack(side=tk.LEFT, padx=4)

        # 狀態燈
        self.lbl_status_light = tk.Label(bottom, text="●", font=("Segoe UI", 14),
                                         fg="#adb5bd", bg="#f0f0f0")
        self.lbl_status_light.pack(side=tk.RIGHT)

        # 禁用所有按鈕直到初始化完成
        self._set_buttons_enabled(False)

    def _set_buttons_enabled(self, enabled: bool) -> None:
        state = tk.NORMAL if enabled else tk.DISABLED
        for btn in (self.btn_1, self.btn_2, self.btn_3, self.btn_4, self.btn_5,
                     self.btn_clear, self.btn_requery, self.btn_path):
            btn.configure(state=state)

    def _set_busy(self, busy: bool, msg: str = "") -> None:
        self.is_busy = busy
        state = tk.DISABLED if busy else tk.NORMAL
        for btn in (self.btn_1, self.btn_2, self.btn_3, self.btn_4, self.btn_5, self.btn_clear):
            btn.configure(state=state)
        # 底部按鈕（重新查詢、路徑）保持可用
        self.btn_requery.configure(state=state)
        self.btn_path.configure(state=state)
        self.lbl_busy.configure(text=msg)
        self.lbl_status_light.configure(fg="#e07c24" if busy else "#2d6a4f")
        self.root.update_idletasks()

    def _show_ip_distribution(self) -> None:
        regions: dict[str, list[str]] = {}
        for svr in self.servers_info:
            r = svr.get("region", "??")
            if r not in regions:
                regions[r] = []
            regions[r].append(f"{svr['ip']} ({svr.get('country', '?')})")

        for r in ("AS", "EU", "NA", "OC"):
            if r in regions:
                desc = "  ".join(regions[r][:2])
                if len(regions[r]) > 2:
                    desc += f" …等 {len(regions[r])} 個"
                self.ip_labels[r].configure(text=desc, fg="#333")
            else:
                self.ip_labels[r].configure(text="—", fg="#888")

    # ─── 初始化 ───

    def _init_session(self) -> None:
        """程式啟動時的背景初始化"""
        # 寫入記錄
        log_raw(f"\n{'='*60}\n=== HG 鎖區工具 GUI v4.0 - {datetime.now():%Y-%m-%d %H:%M:%S} ===\n{'='*60}")

        # 背景執行初始化
        def task() -> None:
            try:
                # 1. 載入或查詢 IP 資訊（自動判斷 7 天快取）
                cfg = load_config()
                if not _should_requery(cfg) and "cached_servers" in cfg:
                    cached = cfg["cached_servers"]
                    self.servers_info = cached
                    last_time = cfg.get("last_query_time", "?")[:10]
                    log_info(f"使用快取 IP 資料（查詢時間: {cfg.get('last_query_time', '?')}）")
                    self.root.after(0, lambda t=last_time: self.lbl_busy.configure(
                        text=f"使用快取 IP 資料（{t}）"))
                else:
                    self.root.after(0, lambda: self.lbl_busy.configure(
                        text="正在查詢伺服器 IP…"))
                    log_info("初始化：查詢 IP 資訊")
                    self.servers_info = []
                    total = len(SERVERS)
                    for i, svr in enumerate(SERVERS, 1):
                        ip = svr["ip"]
                        info = query_ipinfo(ip)
                        if info:
                            self.servers_info.append({
                                "ip": ip,
                                "country": info.get("country", ""),
                                "region": info.get("region", ""),
                                "city": info.get("city", ""),
                                "org": info.get("org", ""),
                                "loc": info.get("loc", ""),
                            })
                            log_info(f"{ip} -> {info.get('country','')}/{info.get('region','')}")
                        else:
                            self.servers_info.append({**svr, "city": "", "org": "", "loc": ""})
                            log_info(f"{ip} 查詢失敗，使用預設: {svr['country']}")
                        if i < total:
                            time.sleep(0.3)

                    # 快取結果
                    _cache_query_result(self.servers_info)

                # 2. 更新 IP 顯示
                self.root.after(0, self._show_ip_distribution)

                # 4. 讀取／選擇路徑
                cfg = load_config()
                saved_path = cfg.get("hn_path", "").replace("/", "\\")
                path_ok = bool(saved_path and all(
                    os.path.isfile(os.path.join(saved_path, f"{app}.exe"))
                    for app in APP_NAMES
                ))

                if path_ok:
                    self.hn_path = saved_path
                    global app_paths_global
                    app_paths_global = {app: os.path.join(saved_path, f"{app}.exe")
                                        for app in APP_NAMES}
                    self.root.after(0, lambda: self.lbl_path.configure(
                        text=f"遊戲路徑: {saved_path}"))
                    log_info(f"使用上次路徑: {saved_path}")
                else:
                    self.root.after(0, self._pick_path_dialog)

                # 5. 更新模式狀態（只接受有效模式）
                saved_mode = cfg.get("last_mode", "")
                if saved_mode in VALID_MODES:
                    self.root.after(0, lambda m=saved_mode: self.lbl_mode.configure(
                        text=f"目前模式: {m}"))

                # 6. 啟用按鈕
                self.root.after(0, lambda: self._set_buttons_enabled(True))
                self.root.after(0, lambda: self.lbl_status_light.configure(fg="#2d6a4f"))

                log_info("初始化完成")
            except Exception as e:
                log_error(f"初始化錯誤: {e}")
                self.root.after(0, lambda err=e: self.lbl_busy.configure(
                    text=f"初始化錯誤: {err}"))

        threading.Thread(target=task, daemon=True).start()

    # ─── 路徑選擇 ───

    def _pick_path_dialog(self) -> None:
        path = filedialog.askdirectory(title="請選擇 HnG 遊戲資料夾")
        if not path:
            self.lbl_busy.configure(text="尚未設定路徑，部分功能受限")
            return

        # filedialog 返回的路徑可能包含正斜杠，netsh 不支援
        path = path.replace("/", "\\")

        missing = [app for app in APP_NAMES
                   if not os.path.isfile(os.path.join(path, f"{app}.exe"))]
        if missing:
            messagebox.showerror("路徑錯誤",
                                 f"找不到以下檔案：\n" +
                                 "\n".join(f"  - {m}.exe" for m in missing) +
                                 "\n\n請確認選擇了正確的 HnG 資料夾。")
            self.lbl_busy.configure(text="路徑錯誤，請重試")
            return

        self.hn_path = path
        global app_paths_global
        app_paths_global = {app: os.path.join(path, f"{app}.exe") for app in APP_NAMES}
        self.lbl_path.configure(text=f"遊戲路徑: {path}")
        save_config(hn_path=path, last_mode=load_config().get("last_mode", ""))
        log_info(f"遊戲路徑: {path}")
        self.lbl_busy.configure(text="路徑已設定")

    # ─── 操作處理 ───

    def _get_hk_ip(self) -> str:
        for s in self.servers_info:
            if s.get("region") == "AS" and "HK" in s.get("country", "").upper():
                return s["ip"]
        return "135.136.10.86"

    def _on_mode(self, mode: int) -> None:
        if self.is_busy:
            return
        if not self.hn_path:
            messagebox.showwarning("未設定路徑", "請先透過「變更路徑」選擇 HnG 遊戲資料夾。")
            return

        mode_names = {
            1: ("僅連亞歐 (AS-EU)", lambda x: x.get("region") in ("NA", "OC"), "AS-EU Only"),
            2: ("僅連歐洲 (EU)", lambda x: x.get("region") != "EU", "EU Only"),
            3: ("僅連亞洲 (AS)", lambda x: x.get("region") != "AS", "AS Only"),
            4: ("僅連香港 (HK)", lambda x: x["ip"] != self._get_hk_ip(), "HK Only"),
            5: ("僅連星歐 (SG+EU)", lambda x: x.get("region") in ("NA", "OC")
                or (x.get("region") == "AS" and "HK" in x.get("country", "").upper()), "SG+EU Only"),
        }
        label, filter_fn, mode_save = mode_names[mode]
        self._run_blocking(label, filter_fn, mode_save)

    def _run_blocking(self, label: str, filter_fn, mode_save: str) -> None:
        self._set_busy(True, f"正在執行 {label}…")

        def task() -> None:
            try:
                log_action(f"開始 {label}")

                # 清除舊規則
                remove_all_rules_silent()
                time.sleep(0.3)

                # 過濾要封鎖的 IP
                block_list = [x for x in self.servers_info if filter_fn(x)]
                total_rules = 0
                for item in block_list:
                    total_rules += add_block_rules_silent(item["ip"], item["country"])

                # 儲存模式
                if self.hn_path:
                    save_config(self.hn_path, mode_save)

                log_action(f"{label} 完成：{len(block_list)} 個 IP，{total_rules} 條規則")

                self.root.after(0, lambda: self.lbl_mode.configure(text=f"目前模式: {mode_save}"))
                self.root.after(0, lambda: messagebox.showinfo(
                    "封鎖完成",
                    f"{label}\n\n"
                    f"已封鎖 {len(block_list)} 個 IP\n"
                    f"共建立 {total_rules} 條防火牆規則\n\n"
                    f"當前模式：{mode_save}"
                ))
            except Exception as e:
                log_error(f"封鎖失敗: {e}")
                self.root.after(0, lambda err=e: messagebox.showerror("錯誤", f"封鎖失敗：{err}"))
            finally:
                self.root.after(0, lambda: self._set_busy(False, "就緒"))

        threading.Thread(target=task, daemon=True).start()

    def _on_clear(self) -> None:
        if self.is_busy:
            return
        if not messagebox.askyesno("確認清除", "確定要移除所有 HG 防火牆規則？"):
            return

        self._set_busy(True, "正在清除規則…")

        def task() -> None:
            try:
                count = remove_all_rules_silent()
                save_config(self.hn_path, "無")
                self.root.after(0, lambda: self.lbl_mode.configure(text="目前模式: 無"))
                log_action("已執行 Clear")
                self.root.after(0, lambda: messagebox.showinfo(
                    "清除完成",
                    f"已移除 {count} 條防火牆規則" if count else "目前無任何 HG 規則"
                ))
            except Exception as e:
                log_error(f"清除失敗: {e}")
                self.root.after(0, lambda err=e: messagebox.showerror("錯誤", f"清除失敗：{err}"))
            finally:
                self.root.after(0, lambda: self._set_busy(False, "就緒"))

        threading.Thread(target=task, daemon=True).start()

    def _on_requery(self) -> None:
        if self.is_busy:
            return
        self._set_busy(True, "正在重新查詢 IP…")

        def task() -> None:
            try:
                new_info = []
                total = len(SERVERS)
                for i, svr in enumerate(SERVERS, 1):
                    ip = svr["ip"]
                    self.root.after(0, lambda m=f"查詢 {i}/{total} {ip}…":
                                    self.lbl_busy.configure(text=m))
                    info = query_ipinfo(ip)
                    if info:
                        new_info.append({
                            "ip": ip,
                            "country": info.get("country", ""),
                            "region": info.get("region", ""),
                            "city": info.get("city", ""),
                            "org": info.get("org", ""),
                            "loc": info.get("loc", ""),
                        })
                        log_info(f"[重新查詢] {ip} -> {info.get('country','')}/{info.get('region','')}")
                    else:
                        new_info.append({**svr, "city": "", "org": "", "loc": ""})
                    if i < total:
                        time.sleep(0.3)

                self.servers_info = new_info
                _cache_query_result(new_info)
                self.root.after(0, self._show_ip_distribution)
                log_action("重新查詢完成")
                self.root.after(0, lambda: messagebox.showinfo("完成", "IP 查詢已完成"))
            except Exception as e:
                log_error(f"重新查詢失敗: {e}")
                self.root.after(0, lambda err=e: messagebox.showerror("錯誤", f"查詢失敗：{err}"))
            finally:
                self.root.after(0, lambda: self._set_busy(False, "就緒"))

        threading.Thread(target=task, daemon=True).start()

    def _on_change_path(self) -> None:
        if self.is_busy:
            return
        self._pick_path_dialog()

    def _open_firewall(self) -> None:
        """開啟 Windows Defender 防火牆進階安全設定"""
        try:
            log_info("使用者開啟 Windows 防火牆")
            subprocess.Popen(["wf.msc"], shell=True)
        except Exception as e:
            log_error(f"開啟防火牆失敗: {e}")
            messagebox.showerror("錯誤", "無法開啟 Windows 防火牆")

    # ─── 啟動 ───

    def run(self) -> None:
        self.root.mainloop()


# ═══════════════════════════════════════════════
# 進入點
# ═══════════════════════════════════════════════

def main() -> None:
    # 檢查管理員權限
    if not is_admin():
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(
            "需要管理員權限",
            "HG 鎖區工具需要管理員權限才能操作防火牆規則。\n\n"
            "將以管理員身分重新啟動…"
        )
        root.destroy()
        run_as_admin()
        return

    app = HGLockerGUI()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        print("\n[!] 發生未預期的錯誤")
        try:
            import msvcrt
            msvcrt.getch()
        except ImportError:
            input()
