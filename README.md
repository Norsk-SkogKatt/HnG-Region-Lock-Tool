# HG 服务器锁区工具 🎯

> Heroes & Generals 服务器锁区工具 — 通过 Windows 防火墙封锁指定地区 IP，自由组合，无需联网查询。

---

## ✨ 功能

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

---

## 🖥️ GUI 版（推荐）

一键操作，无需指令。勾选服务器 → 点击封锁：

```
☑  亚洲（AS）:
  [SG] ☑ 139.99.120.230  (SG-Singapore)
  [HK] ☐ 135.136.10.86   (HK-HongKong)
☐  欧洲（EU）:
      ☐ 147.135.214.90   (FR-Dunkirk)
      ☐ 147.135.252.98   (FR-Dunkirk)
      ...（共 8 个）
☑  北美（NA）:
      ☑ 144.217.77.9     (CA-Quebec)
      ☑ 162.213.248.83   (US-Phoenix)
      ☑ 64.42.180.154    (US-Atlanta)
☐  大洋洲（OC）:
      ☐ 139.99.149.14    (AU-Sydney)

[封锁选中]  [解锁]  [清空所有]
```

### 使用方法

1. **以管理员身份运行**（操作防火墙需要）
2. 首次启动会弹出文件夹选择窗口，请选择 HnG 游戏安装目录（含 `hngsync.exe` 和 `HeroesAndGeneralsDesktop.exe`）
3. 勾选要封锁的服务器 IP，点击「封锁选中」
4. 点击「解锁」可查看并删除指定的规则

---

## ⌨️ CLI 版（TUI）

命令行界面，支持地区码输入，适合批量操作。

```bash
python HG_锁区工具.py
```

启动后进入交互菜单：

```
  [1] 封锁服务器     编号或地区码（如 HK,NA,OC）
  [2] 解锁服务器     从封锁列表中移除规则
  [3] 清空所有规则   移除所有 HG 规则
  [4] 变更路径       重新指定 HnG 文件夹
  [0] 离开
```

### 封锁示例

```
地区码: HK(香港) SG(新加坡) AS(全亚洲) EU(欧洲) NA(北美) OC(大洋洲/AU)

>> HK,NA,OC       ← 封锁香港 + 所有北美 + 所有大洋洲
>> 2,EU           ← 封锁 2 号服务器 + 所有欧洲
>> 1,3,5          ← 封锁第 1、3、5 号服务器
>> A              ← 全选
```

---

## 📋 服务器列表（14 台）

| 区域 | 数量 | 位置 |
|---|---|---|
| 🌏 亚洲 (AS) | 2 | 新加坡、香港 |
| 🌍 欧洲 (EU) | 8 | 法国 Dunkirk(5)、德国 Frankfurt(1)、波兰 Warsaw(1) |
| 🌎 北美 (NA) | 3 | 加拿大 Quebec、美国 Phoenix、美国 Atlanta |
| 🌏 大洋洲 (OC) | 1 | 澳大利亚 Sydney |

> IP 地理位置已硬编码在程序中，无需联网查询，启动即用。

---

## 🔧 技术细节

- **语言**：Python 3.12+
- **依赖**：无第三方包（仅使用标准库）
- **防火墙**：`netsh advfirewall` 双向 (IN+OUT) 全协议封锁
- **GUI 框架**：tkinter（内置）
- **IP 数据**：硬编码在源码中，无需 ipinfo.io 或任何外部 API
- **原版分析**：`Legency 锁区/` 目录包含原版 v2.1 的反编译分析文件

### 防火墙规则命名

```
HG-{IP}({国家})-{程序}-{方向}
```

示例：`HG-139.99.120.230(SG-Singapore)-hngsync-IN`

---

## 📦 从源码构建

### 前置条件

- Python 3.12+
- pip

### 下载源码

```bash
git clone https://github.com/Norsk-SkogKatt/HnG-Region-Lock-Tool.git
cd HnG-Region-Lock-Tool
```

### 直接运行（不打包）

```bash
# CLI 版
python HG_锁区工具.py

# GUI 版
python HG_锁区工具_GUI.py
```

> ⚡ 本项目**无第三方依赖**，仅使用 Python 标准库，下载后即可直接运行。

### 打包成单文件 EXE

使用 PyInstaller 打包为独立 exe，无需 Python 环境即可运行：

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包 CLI 版（需要控制台窗口）
pyinstaller --onefile --clean --console HG_锁区工具.py --name "HG服务器锁定v5.0"

# 打包 GUI 版（无控制台）
pyinstaller --onefile --clean --noconsole HG_锁区工具_GUI.py --name "HG服务器锁定v5.0_GUI"
```

### 参数说明

| 参数 | 说明 |
|---|---|
| `--onefile` | 打包成单个 exe 文件 |
| `--clean` | 清除缓存，确保干净构建 |
| `--console` | 显示控制台窗口（CLI 版必须） |
| `--noconsole` | 不显示控制台窗口（GUI 版使用） |
| `--name` | 指定输出文件名 |

---

## ⚠️ 注意事项

- **需要管理员权限**才能操作 Windows 防火墙
- 封锁前会自动清除旧规则，防止规则冲突
- IP 地理位置由维护者预先查好并硬编码，如有变动请提交 Issue

---

## 📜 许可

MIT License
