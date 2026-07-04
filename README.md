# HG 服务器锁区工具 🎯 / HG Server Region Lock Tool 🎯

> Heroes & Generals 服务器锁区工具 — 通过 Windows 防火墙封锁指定地区 IP，自由组合，无需联网查询。
>
> Heroes & Generals region lock tool — block specific server IPs via Windows Firewall, free combination, no online query needed.

---

## 📖 中文说明

<details>
<summary>点击展开中文说明</summary>

### ✨ 功能

| 功能 | 说明 |
|---|---|
| **自由组合封锁** | 自行勾选/输入要封锁的 IP，支持地区码（HK/SG/AS/EU/NA/OC） |
| **定向解锁** | 查看当前规则，选择要删除的规则 |
| **一键清空** | 删除所有 HG 防火墙规则，恢复原始状态 |
| **双程封锁** | 传入 (IN) + 传出 (OUT) 全协议封锁 |
| **地区硬编码** | IP 地理位置已预设，无需联网查询，即开即用 |
| **自动清除旧规则** | 封锁前自动清除旧规则，避免规则冲突 |
| **路径记忆** | 自动记忆游戏路径，下次启动直接使用 |
| **打开防火墙** | (GUI 版) 一键打开「高级安全 Windows Defender 防火墙」 |
| **中英文切换** | 界面支持中文/英文切换，保存后下次启动自动使用 |

### 🖥️ GUI 版（推荐）

一键操作，无需指令。勾选服务器 → 点击封锁：

`
亚洲（AS）:
  [SG] ☑ 139.99.120.230  (SG-Singapore)
  [HK] ☐ 135.136.10.86   (HK-HongKong)
欧洲（EU）:
      ☐ 147.135.214.90   (FR-Dunkirk)
      ☐ 147.135.252.98   (FR-Dunkirk)
      ...（共 8 个）
北美（NA）:
      ☑ 144.217.77.9     (CA-Quebec)
      ☑ 162.213.248.83   (US-Phoenix)
      ☑ 64.42.180.154    (US-Atlanta)
大洋洲（OC）:
      ☐ 139.99.149.14    (AU-Sydney)

[封锁选中]  [解锁]  [清空所有]
`

#### 使用方法

1. **以管理员身份运行**（操作防火墙需要）
2. 首次启动会弹出文件夹选择窗口，请选择 HnG 游戏安装目录（含 hngsync.exe 和 HeroesAndGeneralsDesktop.exe）
3. 勾选要封锁的服务器 IP，点击「封锁选中」
4. 点击「解锁」可查看并删除指定的规则

### ⌨️ CLI 版（TUI）

命令行界面，支持地区码输入，适合批量操作。

`ash
python HG_锁区工具.py
`

启动后进入交互菜单：

`
  [1] 封锁服务器     编号或地区码（如 HK,NA,OC）
  [2] 解锁服务器     从封锁列表中移除规则
  [3] 清空所有规则   移除所有 HG 规则
  [4] 变更路径       重新指定 HnG 文件夹
  [5] 语言/Language  中英文切换
  [0] 离开
`

#### 封锁示例

`
>> HK,NA,OC       ← 封锁香港 + 所有北美 + 所有大洋洲
>> 2,EU           ← 封锁 2 号服务器 + 所有欧洲
>> 1~5            ← 封锁 1 到 5 号服务器
>> A              ← 全选
`

</details>

---

## 📖 English Documentation

<details>
<summary>Click to expand English documentation</summary>

### ✨ Features

| Feature | Description |
|---|---|
| **Free Combination Block** | Select IPs by checkbox or number input, supports region codes (HK/SG/AS/EU/NA/OC) |
| **Targeted Unblock** | View current rules, select which to delete |
| **One-click Clear** | Delete all HG firewall rules, restore original state |
| **Bidirectional Block** | Inbound (IN) + Outbound (OUT) all-protocol block |
| **Hardcoded Regions** | IP geolocation pre-configured, no online query needed |
| **Auto-clear Old Rules** | Automatically clears old rules before blocking to avoid conflicts |
| **Path Memory** | Remembers game installation path for next launch |
| **Open Firewall** | (GUI version) One-click open "Windows Defender Firewall with Advanced Security" |
| **Language Switch** | Interface supports Chinese/English toggle, persists between sessions |

### 🖥️ GUI Version (Recommended)

One-click operation, no commands needed. Check servers → Click block:

`
Asia (AS):
  [SG] ☑ 139.99.120.230  (SG-Singapore)
  [HK] ☐ 135.136.10.86   (HK-HongKong)
Europe (EU):
      ☐ 147.135.214.90   (FR-Dunkirk)
      ☐ 147.135.252.98   (FR-Dunkirk)
      ...(8 total)
North America (NA):
      ☑ 144.217.77.9     (CA-Quebec)
      ☑ 162.213.248.83   (US-Phoenix)
      ☑ 64.42.180.154    (US-Atlanta)
Oceania (OC):
      ☐ 139.99.149.14    (AU-Sydney)

[Block Selected]  [Unblock]  [Clear All]
`

#### Usage

1. **Run as Administrator** (required for firewall operations)
2. On first launch, browse to your HnG game installation directory (containing hngsync.exe and HeroesAndGeneralsDesktop.exe)
3. Check the server IPs to block, click "Block Selected"
4. Click "Unblock" to view and delete specific rules

### ⌨️ CLI Version (TUI)

Command-line interface supporting region code input, suitable for batch operations.

`ash
python HG_锁区工具.py
`

Interactive menu:

`
  [1] Block Server      Number or region code (e.g. HK,NA,OC)
  [2] Unblock Server    Remove rules from block list
  [3] Clear All Rules   Remove all HG rules
  [4] Change Path       Specify HnG folder again
  [5] 语言/Language     Toggle Chinese/English
  [0] Exit
`

#### Block Examples

`
>> HK,NA,OC       ← Block Hong Kong + all North America + all Oceania
>> 2,EU           ← Block server #2 + all Europe
>> 1~5            ← Block servers 1 through 5
>> A              ← Select all
`

</details>

---

## 📋 Server List / 服务器列表

<details>
<summary>Click to show / 点击查看</summary>

**14 servers total:**

| Region | Count | Locations |
|---|---|---|
| 🌏 Asia (AS) | 2 | Singapore, Hong Kong |
| 🌍 Europe (EU) | 8 | France Dunkirk (5), Germany Frankfurt (1), Poland Warsaw (1) |
| 🌎 North America (NA) | 3 | Canada Quebec, US Phoenix, US Atlanta |
| 🌏 Oceania (OC) | 1 | Australia Sydney |

> IP geolocation is hardcoded in the program. No online query needed.

</details>

---

## 🔧 Technical Details / 技术细节

<details>
<summary>Click to show / 点击查看</summary>

- **Language**: Python 3.12+
- **Dependencies**: None (stdlib only)
- **Firewall**: 
etsh advfirewall bidirectional (IN+OUT) all-protocol block
- **GUI Framework**: tkinter (built-in)
- **IP Data**: Hardcoded in source, no external API needed
- **Original Analysis**: Legency 锁区/ contains decompiled analysis of the original v2.1

### Firewall Rule Naming / 防火墙规则命名

`
HG-{IP}({Country})-{Program}-{Direction}
`

Example: HG-139.99.120.230(SG-Singapore)-hngsync-IN

### Rule Calculation / 规则计算

Each IP × 2 programs (hngsync, HeroesAndGeneralsDesktop) × 2 directions (IN, OUT) = **4 rules per IP**

</details>

---

## 📦 Build from Source / 从源码构建

<details>
<summary>Click to show / 点击查看</summary>

### Prerequisites / 前置条件

- Python 3.12+
- pip

### Download / 下载

`ash
git clone https://github.com/Norsk-SkogKatt/HnG-Region-Lock-Tool.git
cd HnG-Region-Lock-Tool
`

### Run Directly / 直接运行

`ash
# CLI version
python HG_锁区工具.py

# GUI version
python HG_锁区工具_GUI.py
`

> ⚡ No third-party dependencies required. Just download and run.

### Package as EXE / 打包成 EXE

`ash
pip install pyinstaller

# CLI version (needs console window)
pyinstaller --onefile --clean --console HG_锁区工具.py --name "HG服务器锁定v5.0"

# GUI version (no console)
pyinstaller --onefile --clean --noconsole HG_锁区工具_GUI.py --name "HG服务器锁定v5.0_GUI"
`

| Parameter / 参数 | Description / 说明 |
|---|---|
| --onefile | Single exe output |
| --clean | Clean cache before build |
| --console | Show console window (CLI only) |
| --noconsole | Hide console window (GUI only) |
| --name | Output filename |

</details>

---

## ⚠️ Notes / 注意事项

<details>
<summary>Click to show / 点击查看</summary>

- **Admin rights required** to operate Windows Firewall
- Old rules are automatically cleared before creating new ones to prevent conflicts
- IP geolocation is pre-determined and hardcoded; submit an Issue if servers change
- **管理员权限**是操作 Windows 防火墙的必要条件
- 封锁前会自动清除旧规则，防止规则冲突
- IP 地理位置由维护者预先查好并硬编码，如有变动请提交 Issue

</details>

---

## 📜 License / 许可

MIT License
