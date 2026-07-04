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
    print(f"\n[+] 发现 {len(rules)} 条旧规则，正在清除...")
    for name in rules:
        run_netsh(["delete", "rule", f'name={name}'])
        print(f"    已删除: {name}")
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
        print("    无 HG 相关规则")
        return 0
    for i, name in enumerate(rules, 1):
        run_netsh(["delete", "rule", f'name={name}'])
        _show_progress(i, count, f"删除: {name}")
    print(f"\n    已移除 {count} 条规则")
    log_action(f"已移除所有规则 ({count} 条)")
    return count


def show_current_rules() -> None:
    """显示目前的 HG 防火墙规则"""
    rules = get_rule_lines("HG-")
    if rules:
        print(f"\n目前 HG 防火墙规则 ({len(rules)} 条):")
        for name in sorted(rules):
            print(f"  - {name}")
    else:
        print("\n目前无任何 HG 防火墙规则")


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
        print(f"[*] 自动使用上次路径：{saved}")
        log_info(f"使用上次路径: {saved}")
        return saved

    print("\n[?] 请指定 HnG 游戏安装路径")
    path = ""
    while not path:
        raw = input("路径: ").strip().strip("\"'").replace("/", "\\").rstrip("\\")
        path = raw
        if not path:
            print("[!] 路径不得留空")
            continue

        missing = []
        for app in APP_NAMES:
            exe = os.path.join(path, f"{app}.exe")
            if not os.path.isfile(exe):
                missing.append(app)

        if missing:
            print("[!] 找不到以下档案：")
            for m in missing:
                print(f"    - {m}.exe")
            print("    请确认路径后再试。\n")
            retry = input("按 Enter 重试，或输入 Q 离开: ").strip().upper()
            if retry == "Q":
                sys.exit(0)
            path = ""
        else:
            print("\n[✓] 已确认以下程式：")
            for app in APP_NAMES:
                print(f"    {app}.exe")
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
    region_labels = {"AS": "亚洲", "EU": "欧洲", "NA": "北美", "OC": "大洋洲"}

    # 按显示顺序建立 items（地区分组），编号才对得上
    items: list[dict] = []
    for rc in region_order:
        for svr in SERVERS:
            if svr.get("region") == rc:
                items.append(svr)

    print("\n" + "─" * 60)
    print("  选择要封锁的服务器：")
    print("─" * 60)

    idx = 1
    for rc in region_order:
        r_servers = [s for s in items if s.get("region") == rc]
        if not r_servers:
            continue
        label = region_labels.get(rc, rc)
        print(f"\n  {label}（{rc}）:")
        for svr in r_servers:
            ip = svr["ip"]
            country = svr.get("country", "?")
            short = svr.get("short", "")
            tag = f"[{short:>2}] " if short else "     "
            print(f"  {tag}{idx:>2}: {ip}  ({country})")
            idx += 1

    print(f"\n  输入编号、范围或地区码（逗号/空格分隔），A=全选，Enter=返回")
    print(f"  范例:  2~11  或  HK,4~9  或  1,NA,OC  或  A")
    print(f"  地区码: HK(香港) SG(新加坡) AS(全亚洲) EU(欧洲) NA(北美) OC(大洋洲/AU)")
    raw = input("  >> ").strip()
    if not raw:
        return

    selected_indices: set[int] = _parse_region_input(raw, items)
    if not selected_indices:
        print("[!] 未选择有效项目")
        input("按 Enter 返回...")
        return

    selected = [items[i] for i in sorted(selected_indices)]
    total_rules = len(selected) * len(APP_NAMES) * 2
    print(f"\n[+] 将为 {len(selected)} 个 IP 建立 {total_rules} 条规则")

    # 先移除所有现有规则，再建立新的
    print("    -> 正在清除现有规则...")
    removed = remove_all_rules()
    print(f"    已移除 {removed} 条现有规则\n")

    current = 0
    for item in selected:
        current = add_block_rules(item["ip"], item["country"], total_rules, current)

    print()
    show_current_rules()
    print(f"\n[✓] {len(selected)} 个 IP 已双向封锁（传入 + 传出）")
    ips = ", ".join(s["ip"] for s in selected)
    log_action(f"封锁 {len(selected)} 个 IP: {ips}")
    input("按 Enter 返回...")


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
    """将规则列表按基底名称分组（去掉 -IN/-OUT 后缀）。
    返回 [(基底名称, [完整规则名1, 规则名2, ...]), ...] 保持排序。
    """
    groups: dict[str, list[str]] = {}
    for name in rules:
        if name.endswith("-IN"):
            base = name[:-3]
        elif name.endswith("-OUT"):
            base = name[:-4]
        else:
            base = name
        groups.setdefault(base, []).append(name)
    return [(base, groups[base]) for base in sorted(groups)]


def _extract_ip(base: str) -> str:
    """从基底名称中提取 IP，如 HG-135.136.10.86(HK-HongKong)-hngsync → 135.136.10.86"""
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
        print("\n目前无任何 HG 规则")
        input("按 Enter 返回...")
        return

    groups = _group_rules_by_base(rules)
    print(f"\n目前活跃的 HG 规则（{len(groups)} 组，每组含 IN+OUT）:")
    for i, (base, _) in enumerate(groups, 1):
        ip = _extract_ip(base)
        app = base.split("-")[-1] if "-" in base else base
        country_part = base[base.find("("):base.find(")")+1] if "(" in base else ""
        print(f"  [{i:>2}] {ip} {country_part} - {app}")

    print(f"\n  输入编号解锁（逗号/空格分隔，支持范围 2~11），A=全部删除，Enter=返回")
    print(f"  也支持地区码：HK(香港) SG(新加坡) AS(全亚洲) EU(欧洲) NA(北美) OC/AU(大洋洲)")
    raw = input("  >> ").strip()
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
        print("[!] 未选择有效项目")
        input("按 Enter 返回...")
        return

    # 收集所有需要删除的规则（每组删除 IN+OUT 两条）
    to_delete = []
    for i in sorted(selected_indices):
        to_delete.extend(groups[i][1])

    print(f"\n[+] 正在删除 {len(to_delete)} 条规则（{len(selected_indices)} 组）...")
    for i, name in enumerate(to_delete, 1):
        run_netsh(["delete", "rule", f'name={name}'])
        _show_progress(i, len(to_delete), f"删除: {name}")
    print(f"\n[✓] 已删除 {len(to_delete)} 条规则（{len(selected_indices)} 组）")
    log_action(f"解锁: 删除 {len(to_delete)} 条规则（{len(selected_indices)} 组）")
    input("按 Enter 返回...")


# ═══════════════════════════════════════════════
# 介面
# ═══════════════════════════════════════════════

def write_banner() -> None:
    """显示标题画面"""
    os.system("cls")
    print("╔═══════════════════════════════════════════════╗")
    print("║       HG 服务器锁区工具 v5.0                  ║")
    print("║       双向（传入 + 传出）封锁                 ║")
    print("║       自由组合 — 编号 + 地区码混合输入        ║")
    print("╚═══════════════════════════════════════════════╝")
    print("目标程式：hngsync.exe、HeroesAndGeneralsDesktop.exe")
    print("封锁模式：传入 / 传出双向封锁，全协议，全埠")
    print()
    print("规则计算说明：")
    print("  每个 IP × 2 个程式 × 2 方向 = 每 IP 4 条规则")
    print()


def show_ip_distribution() -> None:
    """显示 IP 分布统计"""
    regions: dict[str, list[str]] = {}
    for svr in SERVERS:
        r = svr.get("region", "??")
        if r not in regions:
            regions[r] = []
        regions[r].append(f"{svr['ip']} ({svr.get('country', '?')})")

    print("IP 分布（硬编码地区）：")
    region_labels = {
        "EU": "欧洲",
        "AS": "亚洲",
        "NA": "北美",
        "OC": "大洋洲",
    }
    for r in ["EU", "AS", "NA", "OC"]:
        if r in regions:
            label = region_labels.get(r, r)
            desc = "  ".join(regions[r][:3])
            if len(regions[r]) > 3:
                desc += f"  ...等 {len(regions[r])} 个"
            print(f"  {label}（{r}）  {desc}")
    print()


# ═══════════════════════════════════════════════
# 主程式
# ═══════════════════════════════════════════════

def main() -> None:
    global app_paths

    log_init()
    log_info("使用者授权管理员权限")

    # 检查管理员权限
    if not is_admin():
        print("[!] 需要管理员权限，正在请求...")
        log_info("请求管理员权限")
        run_as_admin()
        return

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
        print("操作：")
        print("  [1] 封锁服务器     编号或地区码（如 HK,NA,OC）")
        print("  [2] 解锁服务器     从封锁列表中移除规则")
        print("  [3] 清空所有规则   移除所有 HG 规则")
        print("  [4] 变更路径       重新指定 HnG 资料夹")
        print("  [0] 离开")

        choice = input("\n请选择 (0-4): ").strip()

        if choice == "1":
            block_servers()
        elif choice == "2":
            unblock_servers()
        elif choice == "3":
            print("\n[+] 正在移除所有防火墙规则...")
            cnt = remove_all_rules()
            print(f"\n[✓] 已移除 {cnt} 条规则")
            log_action("已执行清空所有规则")
            input("按 Enter 返回...")
        elif choice == "4":
            print()
            hn_path = select_hn_root()
            app_paths = {
                app: os.path.join(hn_path, f"{app}.exe")
                for app in APP_NAMES
            }
            print("[✓] 路径已更新")
        elif choice == "0":
            print("\n[-] 再见")
            break
        else:
            print("\n[!] 无效选项")
            input("按 Enter 继续...")


def set_console_size(cols: int = 90, lines: int = 40) -> None:
    """设定主控台视窗大小"""
    try:
        import ctypes
        from ctypes import wintypes

        ctypes.windll.kernel32.SetConsoleTitleW("HG 服务器锁区工具 v5.0")
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
        print("\n[!] 发生未预期的错误，请截图或记录上方红色文字。")
        print("    你也可以检查 HG_lock.log 中的错误日志。")
        print("\n按任意键离开...")
        try:
            import msvcrt
            msvcrt.getch()
        except ImportError:
            input()
