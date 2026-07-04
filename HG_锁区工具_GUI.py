"""
HG 服务器锁区工具 v5.0 (GUI)
透过 Windows 进阶防火墙 (netsh advfirewall) 建立双向封锁规则
自由组合模式 — 复选框选择要封锁的服务器
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ── 服务器 IP 清单（硬编码地区 — 由维护者预先查好） ──
SERVERS: list[dict[str, str]] = [
    {"ip": "139.99.120.230", "region": "AS", "country": "SG-Singapore", "short": "SG"},
    {"ip": "135.136.10.86", "region": "AS", "country": "HK-HongKong", "short": "HK"},
    {"ip": "139.99.149.14", "region": "OC", "country": "AU-Sydney", "short": "OC"},
    {"ip": "144.217.77.9", "region": "NA", "country": "CA-Quebec", "short": ""},
    {"ip": "162.213.248.83", "region": "NA", "country": "US-Phoenix", "short": ""},
    {"ip": "147.135.214.90", "region": "EU", "country": "FR-Dunkirk", "short": ""},
    {"ip": "147.135.252.98", "region": "EU", "country": "FR-Dunkirk", "short": ""},
    {"ip": "149.202.215.48", "region": "EU", "country": "FR-Dunkirk", "short": ""},
    {"ip": "37.187.226.17", "region": "EU", "country": "FR-Dunkirk", "short": ""},
    {"ip": "51.75.119.5", "region": "EU", "country": "FR-Dunkirk", "short": ""},
    {"ip": "51.77.67.200", "region": "EU", "country": "DE-Frankfurt", "short": ""},
    {"ip": "51.83.236.30", "region": "EU", "country": "PL-Warsaw", "short": ""},
    {"ip": "51.91.74.237", "region": "EU", "country": "FR-Dunkirk", "short": ""},
    {"ip": "64.42.180.154", "region": "NA", "country": "US-Atlanta", "short": ""},
]

APP_NAMES: list[str] = ["hngsync", "HeroesAndGeneralsDesktop"]


# ═══════════════════════════════════════════════
# 工具函式（与 CLI 版共用）
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


# ── 防火墙操作 ──

def run_netsh(args: list[str]) -> str:
    cmd = ["netsh", "advfirewall", "firewall"] + args
    log_info(f"执行: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, capture_output=True, timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
        )
        stdout = result.stdout.decode("gbk", errors="replace") if result.stdout else ""
        stderr = result.stderr.decode("gbk", errors="replace") if result.stderr else ""
        if result.returncode != 0:
            log_error(f"netsh 错误: {(stdout + stderr).strip()}")
        return (stdout + stderr).strip()
    except subprocess.TimeoutExpired:
        log_error("netsh 执行超时")
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
        log_action(f"已移除所有规则 ({count} 条)")
    return count


def add_block_rules_silent(ip: str, country: str) -> int:
    """为指定 IP 建立双向封锁规则，回传新增规则数"""
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


# ── 全域状态 ──

app_paths_global: dict[str, str] = {}


# ═══════════════════════════════════════════════
# GUI 应用程式
# ═══════════════════════════════════════════════

class HGLockerGUI:
    """HG 服务器锁区工具 GUI 版"""

    REGION_LABELS = {"EU": "欧洲", "AS": "亚洲", "NA": "北美", "OC": "大洋洲"}

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("HG 服务器锁区工具 v5.0")
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap(default=os.path.join(_get_base_dir(), "icon.ico"))
        except Exception:
            pass

        self.servers_info: list[dict] = []
        self.hn_path: str = ""
        self.is_busy: bool = False  # 锁定按钮防止重复操作

        self._build_ui()
        self._init_session()

    # ─── UI 构建 ───

    def _build_ui(self) -> None:
        self.root.configure(bg="#f0f0f0")

        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        # 标题
        title = tk.Label(main, text="HG 服务器锁区工具", font=("Segoe UI", 18, "bold"),
                         bg="#f0f0f0", fg="#1a1a2e")
        title.pack(pady=(0, 2))

        subtitle = tk.Label(main, text="双向封锁 · 自由组合（勾选要封锁的服务器）", font=("Segoe UI", 9),
                            bg="#f0f0f0", fg="#666")
        subtitle.pack(pady=(0, 8))

        # ── IP 分布显示 ──
        ip_row = ttk.Frame(main)
        ip_row.pack(fill=tk.X, pady=(0, 6))
        self.ip_labels: dict[str, tk.Label] = {}
        for r in ("AS", "EU", "NA", "OC"):
            lbl = tk.Label(ip_row, text=f"{self.REGION_LABELS.get(r, r)}: 查询中...",
                           font=("Segoe UI", 8), bg="#f0f0f0", fg="#888")
            lbl.pack(side=tk.LEFT, padx=(0, 10))
            self.ip_labels[r] = lbl

        # ── 服务器列表（复选框） ──
        self.srv_frame = ttk.LabelFrame(main, text="选择要封锁的服务器", padding=6)
        self.srv_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        self.server_checkboxes: list[tuple[ttk.Checkbutton, tk.BooleanVar, dict]] = []

        # 预留文字（初始化后会被 _populate_servers 取代）
        self._tmp_srv_label = tk.Label(self.srv_frame, text="正在载入服务器资料...",
                                       font=("Segoe UI", 9), fg="#888")
        self._tmp_srv_label.pack(padx=12, pady=8)

        # ── 操作按钮 ──
        action_frame = ttk.Frame(main)
        action_frame.pack(fill=tk.X, pady=(0, 8))

        self.btn_block = tk.Button(action_frame, text="封锁选中", font=("Segoe UI", 11, "bold"),
                                   command=self._on_block, padx=12, pady=4)
        self.btn_block.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_unblock = tk.Button(action_frame, text="解锁", font=("Segoe UI", 11, "bold"),
                                     command=self._on_unlock, padx=12, pady=4)
        self.btn_unblock.pack(side=tk.LEFT, padx=6)

        self.btn_clear = tk.Button(action_frame, text="清空所有", font=("Segoe UI", 11, "bold"),
                                   command=self._on_clear, padx=12, pady=4)
        self.btn_clear.pack(side=tk.LEFT, padx=6)

        # ── 分隔线 ──
        sep = ttk.Separator(main, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=(0, 6))

        # ── 状态列 ──
        status_frame = ttk.Frame(main)
        status_frame.pack(fill=tk.X, pady=(0, 6))

        self.lbl_path = tk.Label(status_frame, text="游戏路径: 尚未设定", font=("Segoe UI", 10),
                                 anchor="w", bg="#f0f0f0")
        self.lbl_path.pack(fill=tk.X)

        self.lbl_busy = tk.Label(status_frame, text="", font=("Segoe UI", 10),
                                 anchor="w", bg="#f0f0f0", fg="#e07c24")
        self.lbl_busy.pack(fill=tk.X)

        # ── 底部按钮列 ──
        bottom = ttk.Frame(main)
        bottom.pack(fill=tk.X)

        self.btn_fw = tk.Button(bottom, text="🛡 开启防火墙", font=("Segoe UI", 10),
                                command=self._open_firewall, padx=8, pady=4)
        self.btn_fw.pack(side=tk.LEFT, padx=(0, 4))

        self.btn_path = tk.Button(bottom, text="📁 变更路径", font=("Segoe UI", 10),
                                  command=self._on_change_path, padx=8, pady=4)
        self.btn_path.pack(side=tk.LEFT, padx=4)

        # 禁用所有按钮直到初始化完成
        self._set_buttons_enabled(False)

    def _set_buttons_enabled(self, enabled: bool) -> None:
        state = tk.NORMAL if enabled else tk.DISABLED
        for btn in (self.btn_block, self.btn_unblock, self.btn_clear,
                     self.btn_path, self.btn_fw):
            btn.configure(state=state)

    def _set_busy(self, busy: bool, msg: str = "") -> None:
        self.is_busy = busy
        state = tk.DISABLED if busy else tk.NORMAL
        for btn in (self.btn_block, self.btn_unblock, self.btn_clear):
            btn.configure(state=state)
        self.btn_path.configure(state=state)
        self.lbl_busy.configure(text=msg)
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
                    desc += f" …等 {len(regions[r])} 个"
                self.ip_labels[r].configure(text=desc, fg="#333")
            else:
                self.ip_labels[r].configure(text="—", fg="#888")

    # ─── 复选框重建（支援地区码分组） ───

    def _populate_servers(self) -> None:
        """根据 self.servers_info 重建服务器复选框"""
        for w in self.srv_frame.winfo_children():
            w.destroy()
        self.server_checkboxes.clear()

        region_order = ["AS", "EU", "NA", "OC"]
        for rc in region_order:
            region_servers = [s for s in self.servers_info if s.get("region") == rc]
            if not region_servers:
                continue
            label = self.REGION_LABELS.get(rc, rc)
            hdr = tk.Label(self.srv_frame, text=f"  {label}（{rc}）:",
                           font=("Segoe UI", 9, "bold"), anchor="w", bg="#f0f0f0")
            hdr.pack(fill=tk.X, pady=(4, 0))
            for svr in region_servers:
                var = tk.BooleanVar(value=False)
                ip = svr["ip"]
                country = svr.get("country", "?")
                short = svr.get("short", "")
                tag = f" [{short}]" if short else "    "
                cb = ttk.Checkbutton(self.srv_frame, text=f"{tag} {ip}  ({country})",
                                     variable=var)
                cb.pack(anchor="w", padx=(24, 0))
                self.server_checkboxes.append((cb, var, svr))

    # ─── 初始化 ───

    def _init_session(self) -> None:
        """程式启动时的背景初始化"""
        # 写入记录
        log_raw(f"\n{'='*60}\n=== HG 锁区工具 GUI v5.0 - {datetime.now():%Y-%m-%d %H:%M:%S} ===\n{'='*60}")

        # 背景执行初始化
        def task() -> None:
            try:
                # 1. 使用硬编码的服务器资料
                self.servers_info = list(SERVERS)
                log_info(f"使用硬编码服务器资料（{len(self.servers_info)} 个 IP）")

                # 2. 更新 IP 显示
                self.root.after(0, self._show_ip_distribution)

                # 3. 建立服务器复选框
                self.root.after(0, self._populate_servers)

                # 4. 读取／选择路径
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
                        text=f"游戏路径: {saved_path}"))
                    log_info(f"使用上次路径: {saved_path}")
                else:
                    self.root.after(0, self._pick_path_dialog)

                # 5. 启用按钮
                self.root.after(0, lambda: self._set_buttons_enabled(True))

                log_info("初始化完成")
            except Exception as e:
                log_error(f"初始化错误: {e}")
                self.root.after(0, lambda err=e: self.lbl_busy.configure(
                    text=f"初始化错误: {err}"))

        threading.Thread(target=task, daemon=True).start()

    # ─── 路径选择 ───

    def _pick_path_dialog(self) -> None:
        path = filedialog.askdirectory(title="请选择 HnG 游戏资料夹")
        if not path:
            self.lbl_busy.configure(text="尚未设定路径，部分功能受限")
            return

        # filedialog 返回的路径可能包含正斜杠，netsh 不支援
        path = path.replace("/", "\\")

        missing = [app for app in APP_NAMES
                   if not os.path.isfile(os.path.join(path, f"{app}.exe"))]
        if missing:
            messagebox.showerror("路径错误",
                                 f"找不到以下档案：\n" +
                                 "\n".join(f"  - {m}.exe" for m in missing) +
                                 "\n\n请确认选择了正确的 HnG 资料夹。")
            self.lbl_busy.configure(text="路径错误，请重试")
            return

        self.hn_path = path
        global app_paths_global
        app_paths_global = {app: os.path.join(path, f"{app}.exe") for app in APP_NAMES}
        self.lbl_path.configure(text=f"游戏路径: {path}")
        save_config(hn_path=path, last_mode=load_config().get("last_mode", ""))
        log_info(f"游戏路径: {path}")
        self.lbl_busy.configure(text="路径已设定")

    # ─── 操作处理 ───

    def _on_block(self) -> None:
        if self.is_busy:
            return
        if not self.hn_path:
            messagebox.showwarning("未设定路径", "请先透过“变更路径”选择 HnG 游戏资料夹。")
            return

        # 收集选中的服务器
        selected = [svr for _, var, svr in self.server_checkboxes if var.get()]
        if not selected:
            messagebox.showinfo("封锁", "请先勾选要封锁的服务器")
            return

        self._set_busy(True, f"正在封锁 {len(selected)} 个 IP…")

        def task() -> None:
            try:
                # 先移除所有现有规则
                removed = remove_all_rules_silent()
                if removed:
                    log_info(f"封锁前已清除 {removed} 条旧规则")
                total_rules = 0
                for item in selected:
                    total_rules += add_block_rules_silent(item["ip"], item["country"])
                log_action(f"封锁 {len(selected)} 个 IP: {', '.join(s['ip'] for s in selected)}")
                self.root.after(0, lambda: messagebox.showinfo(
                    "封锁完成",
                    f"已封锁 {len(selected)} 个 IP\n共建立 {total_rules} 条防火墙规则"
                ))
            except Exception as e:
                log_error(f"封锁失败: {e}")
                self.root.after(0, lambda err=e: messagebox.showerror("错误", f"封锁失败：{err}"))
            finally:
                self.root.after(0, lambda: self._set_busy(False, "就绪"))

        threading.Thread(target=task, daemon=True).start()

    def _on_unlock(self) -> None:
        if self.is_busy:
            return
        rules = get_rule_lines("HG-")
        if not rules:
            messagebox.showinfo("解锁", "目前无任何活跃的 HG 规则")
            return

        # 按基底名称分组（IN/OUT 合并）
        groups: dict[str, list[str]] = {}
        for name in rules:
            if name.endswith("-IN"):
                base = name[:-3]
            elif name.endswith("-OUT"):
                base = name[:-4]
            else:
                base = name
            groups.setdefault(base, []).append(name)
        sorted_bases = sorted(groups)

        # 弹出解锁对话框
        top = tk.Toplevel(self.root)
        top.title("选择要解锁的规则")
        top.transient(self.root)
        top.grab_set()
        top.resizable(False, False)

        tk.Label(top, text="选择要删除的规则（每组含 IN+OUT）：",
                 font=("Segoe UI", 10)).pack(padx=12, pady=(10, 4))

        frame = ttk.Frame(top)
        frame.pack(padx=12, pady=4, fill=tk.BOTH, expand=True)

        base_vars: list[tuple[str, tk.BooleanVar]] = []
        for base in sorted_bases:
            var = tk.BooleanVar(value=False)
            # 美化显示：提取 IP + 国家 + 应用
            display = base.removeprefix("HG-")
            ip = display[:display.find("(")] if "(" in display else display
            country = display[display.find("("):display.find(")")+1] if "(" in display else ""
            app = display.split("-")[-1] if "-" in display else display
            cb = ttk.Checkbutton(frame, text=f"{ip} {country} - {app}", variable=var)
            cb.pack(anchor="w")
            base_vars.append((base, var))

        btn_frame = ttk.Frame(top)
        btn_frame.pack(pady=8)

        def do_delete() -> None:
            selected_bases = [b for b, v in base_vars if v.get()]
            if not selected_bases:
                messagebox.showinfo("解锁", "未选择任何规则", parent=top)
                return

            # 收集所有 IN+OUT 规则
            all_rules = []
            for b in selected_bases:
                all_rules.extend(groups[b])
            if not messagebox.askyesno("确认", f"确定删除 {len(selected_bases)} 组（{len(all_rules)} 条）规则？",
                                       parent=top):
                return

            def task() -> None:
                for name in all_rules:
                    run_netsh(["delete", "rule", f'name={name}'])
                log_action(f"解锁: 删除 {len(all_rules)} 条规则（{len(selected_bases)} 组）")
                self.root.after(0, top.destroy)
                self.root.after(0, lambda: messagebox.showinfo(
                    "完成", f"已删除 {len(all_rules)} 条规则（{len(selected_bases)} 组）"))

            threading.Thread(target=task, daemon=True).start()

        ttk.Button(btn_frame, text="删除选中", command=do_delete).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="取消", command=top.destroy).pack(side=tk.LEFT, padx=4)

    def _on_clear(self) -> None:
        if self.is_busy:
            return
        if not messagebox.askyesno("确认清除", "确定要移除所有 HG 防火墙规则？"):
            return

        self._set_busy(True, "正在清除规则…")

        def task() -> None:
            try:
                count = remove_all_rules_silent()
                log_action("已执行清空所有规则")
                self.root.after(0, lambda: messagebox.showinfo(
                    "清除完成",
                    f"已移除 {count} 条防火墙规则" if count else "目前无任何 HG 规则"
                ))
            except Exception as e:
                log_error(f"清除失败: {e}")
                self.root.after(0, lambda err=e: messagebox.showerror("错误", f"清除失败：{err}"))
            finally:
                self.root.after(0, lambda: self._set_busy(False, "就绪"))

        threading.Thread(target=task, daemon=True).start()

    def _on_change_path(self) -> None:
        if self.is_busy:
            return
        self._pick_path_dialog()

    def _open_firewall(self) -> None:
        """开启 Windows Defender 防火墙进阶安全设定"""
        try:
            log_info("使用者开启 Windows 防火墙")
            subprocess.Popen(["wf.msc"], shell=True)
        except Exception as e:
            log_error(f"开启防火墙失败: {e}")
            messagebox.showerror("错误", "无法开启 Windows 防火墙")

    # ─── 启动 ───

    def run(self) -> None:
        self.root.mainloop()


# ═══════════════════════════════════════════════
# 进入点
# ═══════════════════════════════════════════════

def main() -> None:
    # 检查管理员权限
    if not is_admin():
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(
            "需要管理员权限",
            "HG 锁区工具需要管理员权限才能操作防火墙规则。\n\n"
            "将以管理员身分重新启动…"
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
        print("\n[!] 发生未预期的错误")
        try:
            import msvcrt
            msvcrt.getch()
        except ImportError:
            input()
