"""
HG 服务器锁区工具 v5.0
透过 Windows 进阶防火墙 (netsh advfirewall) 建立双向封锁规则
自由组合模式 — 自行选择要封锁/解锁的服务器（支援地区码）
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime


# ── 多语言支援 ──
LANG: dict[str, dict[str, str]] = {
    "zh": {
        "app_title": "HG 服务器锁区工具 v5.0",
        "console_title": "HG 服务器锁区工具 v5.0",
        "banner_top": "╔═══════════════════════════════════════════════╗",
        "banner_line1": "║       HG 服务器锁区工具 v5.0                  ║",
        "banner_line2": "║       双向（传入 + 传出）封锁                 ║",
        "banner_line3": "║       自由组合 — 编号 + 地区码混合输入        ║",
        "banner_bottom": "╚═══════════════════════════════════════════════╝",
        "banner_targets": "目标程式：hngsync.exe、HeroesAndGeneralsDesktop.exe",
        "banner_mode": "封锁模式：传入 / 传出双向封锁，全协议，全埠",
        "banner_rule_note": "规则计算说明：",
        "banner_rule_detail": "  每个 IP × 2 个程式 × 2 方向 = 每 IP 4 条规则",
        "ip_dist_title": "IP 分布（硬编码地区）：",
        "ip_dist_line": "  {label}（{code}）  {desc}",
        "region_eu": "欧洲",
        "region_as": "亚洲",
        "region_na": "北美",
        "region_oc": "大洋洲",
        "and_more": "...等 {count} 个",
        "rules_title": "\n目前 HG 防火墙规则（{count} 条）:",
        "no_rules": "\n目前无任何 HG 防火墙规则",
        "found_old_rules": "\n[+] 发现 {count} 条旧规则，正在清除...",
        "deleted_rule": "    已删除: {name}",
        "no_hg_rules": "    无 HG 相关规则",
        "removed_rules": "\n    已移除 {count} 条规则",
        "deleting_progress": "删除: {name}",
        "auto_path": "[*] 自动使用上次路径：{path}",
        "ask_path": "\n[?] 请指定 HnG 游戏安装路径",
        "input_path": "路径: ",
        "path_empty": "[!] 路径不得留空",
        "files_missing": "[!] 找不到以下档案：",
        "file_missing_item": "    - {name}.exe",
        "confirm_retry": "    请确认路径后再试。\n",
        "retry_or_quit": "按 Enter 重试，或输入 Q 离开: ",
        "files_confirmed": "\n[✓] 已确认以下程式：",
        "file_confirmed_item": "    {name}.exe",
        "hline": "\n" + "─" * 60,
        "block_title": "  选择要封锁的服务器：",
        "block_hline": "─" * 60,
        "region_header": "\n  {label}（{code}）:",
        "block_select_prompt": "\n  输入编号、范围或地区码（逗号/空格分隔），A=全选，Enter=返回",
        "block_example": "  范例:  2~11  或  HK,4~9  或  1,NA,OC  或  A",
        "block_region_codes": "  地区码: HK(香港) SG(新加坡) AS(全亚洲) EU(欧洲) NA(北美) OC(大洋洲/AU)",
        "block_input_prompt": "  >> ",
        "block_no_selection": "[!] 未选择有效项目",
        "will_create_rules": "\n[+] 将为 {count} 个 IP 建立 {total} 条规则",
        "clearing_rules": "    -> 正在清除现有规则...",
        "removed_existing": "    已移除 {count} 条现有规则\n",
        "block_done": "\n[✓] {count} 个 IP 已双向封锁（传入 + 传出）",
        "press_enter_return": "按 Enter 返回...",
        "no_hg_rules_unblock": "\n目前无任何 HG 规则",
        "unblock_title": "\n目前活跃的 HG 规则（{groups} 组，每组含 IN/OUT × 两个程序 = 4 条规则）:",
        "unblock_select_prompt": "\n  输入编号解锁（逗号/空格分隔，支持范围 2~11），A=全部删除，Enter=返回",
        "unblock_region_codes": "  也支持地区码：HK(香港) SG(新加坡) AS(全亚洲) EU(欧洲) NA(北美) OC/AU(大洋洲)",
        "unblock_input_prompt": "  >> ",
        "unblock_no_selection": "\n[!] 未选择有效项目",
        "unblock_deleting": "\n[+] 正在删除 {total} 条规则（{servers} 个服务器）...",
        "unblock_done": "\n[✓] 已删除 {total} 条规则（{servers} 个服务器）",
        "need_admin": "[!] 需要管理员权限，正在请求...",
        "menu_header": "操作：",
        "menu_block": "  [1] 封锁服务器     编号或地区码（如 HK,NA,OC）",
        "menu_unblock": "  [2] 解锁服务器     从封锁列表中移除规则",
        "menu_clear": "  [3] 清空所有规则   移除所有 HG 规则",
        "menu_change_path": "  [4] 变更路径       重新指定 HnG 资料夹",
        "menu_lang": "  [5] 语言/Language",
        "menu_exit": "  [0] 离开",
        "menu_choice": "\n请选择 (0-5): ",
        "clearing_all_rules": "\n[+] 正在移除所有防火墙规则...",
        "cleared_all_rules": "\n[✓] 已移除 {count} 条规则",
        "path_updated": "\n[✓] 路径已更新",
        "goodbye": "\n[-] 再见",
        "invalid_option": "\n[!] 无效选项",
        "press_enter_continue": "按 Enter 继续...",
        "error_unexpected": "\n[!] 发生未预期的错误，请截图或记录上方红色文字。",
        "error_check_log": "    你也可以检查 HG_lock.log 中的错误日志。",
        "press_any_key": "\n按任意键离开...",
        "lang_switched": "\n[✓] 语言已切换为 English",
    },
    "en": {
        "app_title": "HG Server Region Lock Tool v5.0",
        "console_title": "HG Server Region Lock Tool v5.0",
        "banner_top": "╔═══════════════════════════════════════════════╗",
        "banner_line1": "║       HG Server Region Lock Tool v5.0         ║",
        "banner_line2": "║       Bidirectional (In + Out) Lock           ║",
        "banner_line3": "║       Free Combo — Number + Region Code Input ║",
        "banner_bottom": "╚═══════════════════════════════════════════════╝",
        "banner_targets": "Targets: hngsync.exe, HeroesAndGeneralsDesktop.exe",
        "banner_mode": "Block Mode: Bidirectional In/Out, All Protocols, All Ports",
        "banner_rule_note": "Rule Calculation:",
        "banner_rule_detail": "  Each IP × 2 programs × 2 directions = 4 rules per IP",
        "ip_dist_title": "IP Distribution (hardcoded regions):",
        "ip_dist_line": "  {label} ({code})  {desc}",
        "region_eu": "Europe",
        "region_as": "Asia",
        "region_na": "North America",
        "region_oc": "Oceania",
        "and_more": "...and {count} more",
        "rules_title": "\nCurrent HG firewall rules ({count}):",
        "no_rules": "\nNo HG firewall rules currently",
        "found_old_rules": "\n[+] Found {count} old rules, cleaning up...",
        "deleted_rule": "    Deleted: {name}",
        "no_hg_rules": "    No HG-related rules",
        "removed_rules": "\n    Removed {count} rules",
        "deleting_progress": "Deleting: {name}",
        "auto_path": "[*] Auto-using last path: {path}",
        "ask_path": "\n[?] Please specify HnG game installation path",
        "input_path": "Path: ",
        "path_empty": "[!] Path cannot be empty",
        "files_missing": "[!] Cannot find the following files:",
        "file_missing_item": "    - {name}.exe",
        "confirm_retry": "    Please verify the path and try again.\n",
        "retry_or_quit": "Press Enter to retry, or input Q to quit: ",
        "files_confirmed": "\n[✓] Confirmed the following programs:",
        "file_confirmed_item": "    {name}.exe",
        "hline": "\n" + "─" * 60,
        "block_title": "  Select servers to block:",
        "block_hline": "─" * 60,
        "region_header": "\n  {label} ({code}):",
        "block_select_prompt": "\n  Input number, range, or region code (comma/space separated), A=Select All, Enter=Back",
        "block_example": "  Examples: 2~11  or  HK,4~9  or  1,NA,OC  or  A",
        "block_region_codes": "  Codes: HK(Hong Kong) SG(Singapore) AS(All Asia) EU(Europe) NA(North America) OC(Oceania/AU)",
        "block_input_prompt": "  >> ",
        "block_no_selection": "[!] No valid items selected",
        "will_create_rules": "\n[+] Will create {total} rules for {count} IPs",
        "clearing_rules": "    -> Clearing existing rules...",
        "removed_existing": "    Removed {count} existing rules\n",
        "block_done": "\n[✓] {count} IPs blocked bidirectionally (In + Out)",
        "press_enter_return": "Press Enter to return...",
        "no_hg_rules_unblock": "\nNo HG rules currently",
        "unblock_title": "\nCurrently active HG rules ({groups} groups, each with IN/OUT × 2 programs = 4 rules):",
        "unblock_select_prompt": "\n  Input number to unblock (comma/space separated, supports range 2~11), A=Delete All, Enter=Back",
        "unblock_region_codes": "  Also supports region codes: HK(Hong Kong) SG(Singapore) AS(All Asia) EU(Europe) NA(North America) OC/AU(Oceania)",
        "unblock_input_prompt": "  >> ",
        "unblock_no_selection": "\n[!] No valid items selected",
        "unblock_deleting": "\n[+] Deleting {total} rules ({servers} servers)...",
        "unblock_done": "\n[✓] Deleted {total} rules ({servers} servers)",
        "need_admin": "[!] Admin privileges required, requesting...",
        "menu_header": "Operations:",
        "menu_block": "  [1] Block Server     Number or region code (e.g. HK,NA,OC)",
        "menu_unblock": "  [2] Unblock Server   Remove rules from block list",
        "menu_clear": "  [3] Clear All Rules  Remove all HG rules",
        "menu_change_path": "  [4] Change Path      Specify HnG folder again",
        "menu_lang": "  [5] 语言/Language",
        "menu_exit": "  [0] Exit",
        "menu_choice": "\nPlease choose (0-5): ",
        "clearing_all_rules": "\n[+] Removing all firewall rules...",
        "cleared_all_rules": "\n[✓] Removed {count} rules",
        "path_updated": "\n[✓] Path updated",
        "goodbye": "\n[-] Goodbye",
        "invalid_option": "\n[!] Invalid option",
        "press_enter_continue": "Press Enter to continue...",
        "error_unexpected": "\n[!] An unexpected error occurred. Please screenshot or note the red text above.",
        "error_check_log": "    You can also check HG_lock.log for error logs.",
        "press_any_key": "\nPress any key to exit...",
        "lang_switched": "\n[✓] Language switched to 中文",
    },
}
current_lang: str = "zh"


def _(key: str) -> str:
    return LANG.get(current_lang, {}).get(key, LANG["zh"].get(key, key))


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

# ── 全域状态 ──
LOG_FILE: str = ""
CONFIG_FILE: str = ""
app_paths: dict[str, str] = {}


# ═══════════════════════════════════════════════
# 工具函式
# ═══════════════════════════════════════════════

def _get_base_dir() -> str:
    """取得程式所在目录（支援 PyInstaller 打包）"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def log_init() -> None:
    """初始化记录档"""
    global LOG_FILE
    base = _get_base_dir()
    LOG_FILE = os.path.join(base, "HG_lock.log")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"=== HG 锁区工具 v5.0 - {datetime.now():%Y-%m-%d %H:%M:%S} ===\n")
        f.write(f"{'='*60}\n")


def log_raw(text: str) -> None:
    """写入原始文字到记录档"""
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
# 设定档管理
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
    cfg["lang"] = current_lang
    cfg["last_updated"] = datetime.now().isoformat()
    try:
        with open(_config_path(), "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


# ═══════════════════════════════════════════════
# 管理员权限
# ═══════════════════════════════════════════════

def is_admin() -> bool:
    """检查是否以管理员权限执行"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except (ImportError, AttributeError):
        return False


def run_as_admin() -> None:
    """以管理员权限重启程式"""
    import ctypes
    script = sys.argv[0]
    params = " ".join(sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1
    )


# ═══════════════════════════════════════════════
# 防火墙操作（netsh advfirewall）
# ═══════════════════════════════════════════════

def run_netsh(args: list[str]) -> str:
    """执行 netsh 命令并回传输出"""
    cmd = ["netsh", "advfirewall", "firewall"] + args
    log_info(f"执行: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, capture_output=True, timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
        )
        stdout = result.stdout.decode("gbk", errors="replace") if result.stdout else ""
        stderr = result.stderr.decode("gbk", errors="replace") if result.stderr else ""
        output = stdout + stderr
        if result.returncode != 0:
            log_error(f"netsh 错误: {output.strip()}")
        return output.strip()
    except subprocess.TimeoutExpired:
        log_error("netsh 执行超时")
        return ""
    except FileNotFoundError:
        log_error("找不到 netsh.exe，请确认 Windows 防火墙可用")
        return ""


def get_rule_lines(keyword: str = "HG-") -> list[str]:
    """取得所有符合关键字的防火墙规则名称"""
    output = run_netsh(["show", "rule", "name=all"])
    names: list[str] = []
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
    """移除旧版规则（v1/v2 格式）"""
    rules = get_rule_lines("HG-")
    if not rules:
        return
    print(_("found_old_rules").format(count=len(rules)))
    for name in rules:
        run_netsh(["delete", "rule", f'name={name}'])
        print(_("deleted_rule").format(name=name))
    log_action(f"已清除 {len(rules)} 条旧规则")


def add_block_rules(
    ip: str, country: str, total: int = 0, current: int = 0
) -> int:
    """为指定 IP 在每个目标程式上建立双向封锁规则"""
    for app in APP_NAMES:
        name_in = f"HG-{ip}({country})-{app}-IN"
        name_out = f"HG-{ip}({country})-{app}-OUT"
        prog = app_paths.get(app, "")

        # 新增传入规则
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

        # 新增传出规则
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
    """显示进度条"""
    bar_width = 30
    filled = bar_width * current // total
    bar = "█" * filled + "░" * (bar_width - filled)
    pct = 100 * current // total
    print(f"\r    [{bar}] {pct:>3}%  {label}", end="", flush=True)
    if current >= total:
        print()


def remove_all_rules() -> int:
    """移除所有 HG 相关的防火墙规则"""
    rules = get_rule_lines("HG-")
    count = len(rules)
    if not rules:
        print(_("no_hg_rules"))
        return 0
    for i, name in enumerate(rules, 1):
        run_netsh(["delete", "rule", f'name={name}'])
        _show_progress(i, count, _("deleting_progress").format(name=name))
    print(_("removed_rules").format(count=count))
    log_action(f"已移除所有规则 ({count} 条)")
    return count


def show_current_rules() -> None:
    """显示目前的 HG 防火墙规则"""
    rules = get_rule_lines("HG-")
    if rules:
        print(_("rules_title").format(count=len(rules)))
        for name in sorted(rules):
            print(f"  - {name}")
    else:
        print(_("no_rules"))


# ═══════════════════════════════════════════════
# 游戏路径选择
# ═══════════════════════════════════════════════

def select_hn_root() -> str:
    """选择 Heroes & Generals 游戏安装路径"""
    cfg = load_config()
    saved = cfg.get("hn_path", "").replace("/", "\\")

    if saved and all(
        os.path.isfile(os.path.join(saved, f"{app}.exe"))
        for app in APP_NAMES
    ):
        print(_("auto_path").format(path=saved))
        log_info(f"使用上次路径: {saved}")
        return saved

    print(_("ask_path"))
    path = ""
    while not path:
        raw = input(_("input_path")).strip().strip("\"'").replace("/", "\\").rstrip("\\")
        path = raw
        if not path:
            print(_("path_empty"))
            continue

        missing = []
        for app in APP_NAMES:
            exe = os.path.join(path, f"{app}.exe")
            if not os.path.isfile(exe):
                missing.append(app)

        if missing:
            print(_("files_missing"))
            for m in missing:
                print(_("file_missing_item").format(name=m))
            print(_("confirm_retry"))
            retry = input(_("retry_or_quit")).strip().upper()
            if retry == "Q":
                sys.exit(0)
            path = ""
        else:
            print(_("files_confirmed"))
            for app in APP_NAMES:
                print(_("file_confirmed_item").format(name=app))
            log_info(f"游戏路径: {path}")
            save_config(hn_path=path, last_mode=cfg.get("last_mode", ""))
            return path

    return ""  # unreachable


# ═══════════════════════════════════════════════
# 封锁逻辑
# ═══════════════════════════════════════════════

# 地区码 → 匹配规则
REGION_CODES: dict[str, str] = {
    "AS": "AS", "EU": "EU", "NA": "NA", "OC": "OC",
    "HK": "country", "SG": "country", "AU": "OC",
}


def block_servers() -> None:
    """自由选择要封锁的服务器（支援编号 + 地区码组合）"""
    region_order = ["AS", "EU", "NA", "OC"]
    region_labels = {
        "AS": _("region_as"),
        "EU": _("region_eu"),
        "NA": _("region_na"),
        "OC": _("region_oc"),
    }

    # 按显示顺序建立 items（地区分组），编号才对得上
    items: list[dict] = []
    for rc in region_order:
        for svr in SERVERS:
            if svr.get("region") == rc:
                items.append(svr)

    print(_("hline"))
    print(_("block_title"))
    print(_("block_hline"))

    idx = 1
    for rc in region_order:
        r_servers = [s for s in items if s.get("region") == rc]
        if not r_servers:
            continue
        label = region_labels.get(rc, rc)
        print(_("region_header").format(label=label, code=rc))
        for svr in r_servers:
            ip = svr["ip"]
            country = svr.get("country", "?")
            short = svr.get("short", "")
            tag = f"[{short:>2}] " if short else "     "
            print(f"  {tag}{idx:>2}: {ip}  ({country})")
            idx += 1

    print(_("block_select_prompt"))
    print(_("block_example"))
    print(_("block_region_codes"))
    raw = input(_("block_input_prompt")).strip()
    if not raw:
        return

    selected_indices: set[int] = _parse_region_input(raw, items)
    if not selected_indices:
        print(_("block_no_selection"))
        input(_("press_enter_return"))
        return

    selected = [items[i] for i in sorted(selected_indices)]
    total_rules = len(selected) * len(APP_NAMES) * 2
    print(_("will_create_rules").format(count=len(selected), total=total_rules))

    # 先移除所有现有规则，再建立新的
    print(_("clearing_rules"))
    removed = remove_all_rules()
    print(_("removed_existing").format(count=removed))

    current = 0
    for item in selected:
        current = add_block_rules(item["ip"], item["country"], total_rules, current)

    print()
    show_current_rules()
    print(_("block_done").format(count=len(selected)))
    ips = ", ".join(s["ip"] for s in selected)
    log_action(f"封锁 {len(selected)} 个 IP: {ips}")
    input(_("press_enter_return"))


def _parse_range_token(token: str, item_count: int) -> set[int]:
    """解析单个标记：数字 或 范围（2~11/2-11），回传 0-index 索引集合"""
    result: set[int] = set()
    t = token.strip()
    if "~" in t or "-" in t:
        sep = "~" if "~" in t else "-"
        parts = t.split(sep, 1)
        try:
            start = int(parts[0].strip()) - 1
            end = int(parts[1].strip()) - 1
            if start < 0:
                start = 0
            if end >= item_count:
                end = item_count - 1
            if start <= end:
                for n in range(start, end + 1):
                    result.add(n)
        except ValueError:
            pass
    else:
        try:
            n = int(t) - 1
            if 0 <= n < item_count:
                result.add(n)
        except ValueError:
            pass
    return result


def _parse_region_input(raw: str, items: list[dict]) -> set[int]:
    """解析使用者输入：支援编号、范围（2~11）、地区码、组合"""
    selected: set[int] = set()
    if raw.upper() == "A":
        return set(range(len(items)))

    for part in raw.replace(",", " ").split():
        t = part.strip()
        # 范围或数字
        result = _parse_range_token(t, len(items))
        if result:
            selected.update(result)
            continue

        t_upper = t.upper()
        # 地区码
        if t_upper in ("AS", "EU", "NA", "OC"):
            for i, svr in enumerate(items):
                if svr.get("region") == t_upper:
                    selected.add(i)
        elif t_upper == "HK":
            for i, svr in enumerate(items):
                if svr.get("country", "").startswith("HK"):
                    selected.add(i)
        elif t_upper == "SG":
            for i, svr in enumerate(items):
                if svr.get("country", "").startswith("SG"):
                    selected.add(i)
        elif t_upper in ("AU",):
            for i, svr in enumerate(items):
                if svr.get("region") == "OC":
                    selected.add(i)

    return selected


def _group_rules_by_base(rules: list[str]) -> list[tuple[str, list[str]]]:
    """将规则按服务器（IP+国家）分组，合并 IN/OUT + hngsync/desktop。
    返回 [(服务器键, [完整规则名1, ...]), ...] 保持排序。
    """
    groups: dict[str, list[str]] = {}
    for name in rules:
        # 去掉 -IN/-OUT
        if name.endswith("-IN"):
            stem = name[:-3]
        elif name.endswith("-OUT"):
            stem = name[:-4]
        else:
            stem = name
        # 去掉 app 名称（最后一个 ) 后面的部分）
        # stem = HG-IP(country)-app → key = HG-IP(country)
        idx = stem.rfind(")")
        key = stem[: idx + 1] if idx > 0 else stem
        groups.setdefault(key, []).append(name)
    return [(key, groups[key]) for key in sorted(groups)]


def _extract_ip(base: str) -> str:
    """从基底名称中提取 IP，如 HG-135.136.10.86(HK-HongKong) → 135.136.10.86"""
    s = base.removeprefix("HG-")
    idx = s.find("(")
    return s[:idx] if idx > 0 else s


def _match_rule_base_to_region(base: str, code: str) -> bool:
    """判断基底名称是否匹配地区码"""
    code_upper = code.upper()
    if code_upper in ("OC", "AU"):
        return "(AU-" in base
    if code_upper == "AS":
        return "(HK-" in base or "(SG-" in base
    if code_upper == "HK":
        return "(HK-" in base
    if code_upper == "SG":
        return "(SG-" in base
    if code_upper == "EU":
        for prefix in ("(FR-", "(DE-", "(PL-"):
            if prefix in base:
                return True
        return False
    if code_upper == "NA":
        return "(CA-" in base or "(US-" in base
    return False


def unblock_servers() -> None:
    """自由选择要解锁的防火墙规则（IN/OUT 合并为一组）"""
    rules = get_rule_lines("HG-")
    if not rules:
        print(_("no_hg_rules_unblock"))
        input(_("press_enter_return"))
        return

    groups = _group_rules_by_base(rules)
    print(_("unblock_title").format(groups=len(groups)))
    for i, (base, _) in enumerate(groups, 1):
        ip = _extract_ip(base)
        country_part = base[base.find("("):base.find(")")+1] if "(" in base else ""
        print(f"  [{i:>2}] {ip} {country_part}")

    print(_("unblock_select_prompt"))
    print(_("unblock_region_codes"))
    raw = input(_("unblock_input_prompt")).strip()
    if not raw:
        return

    selected_indices: set[int] = set()
    if raw.upper() == "A":
        selected_indices = set(range(len(groups)))
    else:
        for part in raw.replace(",", " ").split():
            t = part.strip()
            # 数字或范围
            result = _parse_range_token(t, len(groups))
            if result:
                selected_indices.update(result)
                continue
            # 地区码
            t_upper = t.upper()
            for i, (base, _) in enumerate(groups):
                if _match_rule_base_to_region(base, t_upper):
                    selected_indices.add(i)

    if not selected_indices:
        print(_("unblock_no_selection"))
        input(_("press_enter_return"))
        return

    # 收集所有需要删除的规则（每组删除 IN+OUT 两条）
    to_delete = []
    for i in sorted(selected_indices):
        to_delete.extend(groups[i][1])

    print(_("unblock_deleting").format(total=len(to_delete), servers=len(selected_indices)))
    for i, name in enumerate(to_delete, 1):
        run_netsh(["delete", "rule", f'name={name}'])
        _show_progress(i, len(to_delete), _("deleting_progress").format(name=name))
    print(_("unblock_done").format(total=len(to_delete), servers=len(selected_indices)))
    log_action(f"解锁: 删除 {len(to_delete)} 条规则（{len(selected_indices)} 个服务器）")
    input(_("press_enter_return"))


# ═══════════════════════════════════════════════
# 介面
# ═══════════════════════════════════════════════

def write_banner() -> None:
    """显示标题画面"""
    os.system("cls")
    print(_("banner_top"))
    print(_("banner_line1"))
    print(_("banner_line2"))
    print(_("banner_line3"))
    print(_("banner_bottom"))
    print(_("banner_targets"))
    print(_("banner_mode"))
    print()
    print(_("banner_rule_note"))
    print(_("banner_rule_detail"))
    print()


def show_ip_distribution() -> None:
    """显示 IP 分布统计"""
    regions: dict[str, list[str]] = {}
    for svr in SERVERS:
        r = svr.get("region", "??")
        if r not in regions:
            regions[r] = []
        regions[r].append(f"{svr['ip']} ({svr.get('country', '?')})")

    print(_("ip_dist_title"))
    region_labels = {
        "EU": _("region_eu"),
        "AS": _("region_as"),
        "NA": _("region_na"),
        "OC": _("region_oc"),
    }
    for r in ["EU", "AS", "NA", "OC"]:
        if r in regions:
            label = region_labels.get(r, r)
            desc = "  ".join(regions[r][:3])
            if len(regions[r]) > 3:
                desc += _("and_more").format(count=len(regions[r]))
            print(_("ip_dist_line").format(label=label, code=r, desc=desc))
    print()


# ═══════════════════════════════════════════════
# 主程式
# ═══════════════════════════════════════════════

def main() -> None:
    global app_paths, current_lang

    log_init()
    log_info("使用者授权管理员权限")

    # 检查管理员权限
    if not is_admin():
        print(_("need_admin"))
        log_info("请求管理员权限")
        run_as_admin()
        return

    cfg = load_config()
    current_lang = cfg.get("lang", "zh")

    set_console_size()

    # 选择游戏路径
    hn_path = select_hn_root()
    app_paths = {
        app: os.path.join(hn_path, f"{app}.exe")
        for app in APP_NAMES
    }

    # 主选单回圈
    while True:
        write_banner()
        show_ip_distribution()
        print()
        print(_("menu_header"))
        print(_("menu_block"))
        print(_("menu_unblock"))
        print(_("menu_clear"))
        print(_("menu_change_path"))
        print(_("menu_lang"))
        print(_("menu_exit"))

        choice = input(_("menu_choice")).strip()

        if choice == "1":
            block_servers()
        elif choice == "2":
            unblock_servers()
        elif choice == "3":
            print(_("clearing_all_rules"))
            cnt = remove_all_rules()
            print(_("cleared_all_rules").format(count=cnt))
            log_action("已执行清空所有规则")
            input(_("press_enter_return"))
        elif choice == "4":
            print()
            hn_path = select_hn_root()
            app_paths = {
                app: os.path.join(hn_path, f"{app}.exe")
                for app in APP_NAMES
            }
            print(_("path_updated"))
        elif choice == "5":
            current_lang = "en" if current_lang == "zh" else "zh"
            save_config()
            print(_("lang_switched"))
            input(_("press_enter_continue"))
        elif choice == "0":
            print(_("goodbye"))
            break
        else:
            print(_("invalid_option"))
            input(_("press_enter_continue"))


def set_console_size(cols: int = 90, lines: int = 40) -> None:
    """设定主控台视窗大小"""
    try:
        import ctypes
        from ctypes import wintypes

        ctypes.windll.kernel32.SetConsoleTitleW(_("console_title"))
        os.system(f"mode con cols={cols} lines={lines}")

        h = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        buf = wintypes.COORD(cols, 3000)
        ctypes.windll.kernel32.SetConsoleScreenBufferSize(h, buf)
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        print(_("error_unexpected"))
        print(_("error_check_log"))
        print(_("press_any_key"))
        try:
            import msvcrt
            msvcrt.getch()
        except ImportError:
            input()
