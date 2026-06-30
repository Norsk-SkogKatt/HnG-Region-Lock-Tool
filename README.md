# HG 伺服器鎖區工具 🎯

> Heroes & Generals 伺服器鎖區工具 — 透過 Windows 防火牆封鎖指定地區 IP，降低延遲、改善連線品質。

原版 `HG服务器锁定v2.1.exe`（PyInstaller 打包）經反編譯分析後重新實作，採用 **ipinfo.io** 動態 IP 地理查詢取代原版硬編碼，並提供 **GUI 版** 與 **CLI 版** 兩種介面。

---

## ✨ 功能

| 功能 | 說明 |
|---|---|
| **AS-EU Only** | 只留亞洲 + 歐洲，封鎖北美 + 大洋洲 |
| **EU Only** | 封鎖歐洲以外所有 IP |
| **AS Only** | 封鎖亞洲以外所有 IP |
| **HK Only** | 僅連接香港，封鎖其餘所有 IP |
| **清除規則** | 一鍵移除所有 HG 防火牆規則 |
| **重新查詢** | 重新透過 ipinfo.io 查詢伺服器地理位置 |
| **IP 查詢** | 開機自動查詢 13 台伺服器 IP 所屬地區 |
| **雙向封鎖** | 傳入 (IN) + 傳出 (OUT) 全協議封鎖 |
| **設定持久化** | 自動記憶上次模式與遊戲路徑 |
| **開啟防火牆** | (GUI 版) 一鍵開啟「進階安全 Windows Defender 防火牆」 |

---

## 🖥️ GUI 版（推薦）

![GUI 截圖](screenshot.png)

一鍵操作，無需指令。點擊對應按鈕即自動完成：

```
① AS-EU Only    ② EU Only
③ AS Only       ④ HK Only

[⑤ 清除所有規則]

[🛡 開啟防火牆] [🔄 重新查詢] [📁 變更路徑]
```

### 使用方法

1. **以管理員身分執行**（操作防火牆需要）
2. 首次啟動會自動：
   - 查詢 13 台伺服器的 IP 地理位置
   - 彈出資料夾選擇視窗，請選取 HnG 遊戲安裝目錄（含 `hngsync.exe` 和 `HeroesAndGeneralsDesktop.exe`）
3. 點擊對應按鈕即可切換鎖區模式

> 💡 點擊右下角「🛡 開啟防火牆」可直達「進階安全 Windows Defender 防火牆」檢查已建立的規則。

---

## ⌨️ CLI 版

傳統命令列介面，適合進階使用者。

```bash
python HG_锁区工具.py
```

啟動後會進入互動選單：

```
[1] AS-EU Only   只留亞洲 + 歐洲，封鎖北美 + 大洋洲
[2] EU Only      封鎖歐洲以外所有 IP
[3] AS Only      封鎖亞洲以外所有 IP
[4] HK Only      僅連接香港，封鎖其餘所有 IP
[5] Clear        移除所有 HG 防火牆規則
[6] 重新查詢     重新透過 ipinfo.io 查詢 IP 位置
[7] 變更路徑     重新指定 HnG 資料夾
[0] 離開
```

---

## 📋 伺服器列表

共 13 台伺服器，涵蓋四大區域：

| 區域 | 數量 | 位置 |
|---|---|---|
| 🌏 亞洲 (AS) | 2 | 新加坡、香港 |
| 🌍 歐洲 (EU) | 8 | 法國(5)、德國(1)、波蘭(1) |
| 🌎 北美 (NA) | 2 | 加拿大魁北克、美國鳳凰城 |
| 🌏 大洋洲 (OC) | 1 | 澳洲雪梨 |

---

## 🔧 技術細節

- **語言**：Python 3.12+
- **依賴**：無第三方套件（僅使用標準函式庫）
- **防火牆**：`netsh advfirewall` 雙向 (IN+OUT) 全協議封鎖
- **IP 查詢**：[ipinfo.io](https://ipinfo.io) API（可選填 Token 提升配額）
- **GUI 框架**：tkinter（內建）
- **原始碼分析**：`Legency 锁区/` 目錄包含原版 v2.1 的反編譯分析文件

### 防火牆規則命名

```
HG-{IP}({國家})-{程式}-{方向}
```

範例：`HG-139.99.120.230(SG-Singapore)-hngsync-IN`

---

## 📦 打包成單檔 EXE

```bash
pip install pyinstaller
pyinstaller --onefile --clean --nowindowed HG_锁区工具.py --name HG服务器锁定v3.0.exe
pyinstaller --onefile --clean --nowindowed HG_锁区工具_GUI.py --name HG服务器锁定v4.0_GUI.exe
```

---

## ⚠️ 注意事項

- **需要管理員權限**才能操作 Windows 防火牆
- ipinfo.io 免費版每月配額 50,000 次請求，本工具每次啟動查詢 13 次
- 若遇到 IP 查詢失敗，會自動使用預設地區資料
- 建議定期使用「重新查詢」更新 IP 地理位置（伺服器 IP 可能會變動）

---

## 📜 授權

MIT License

---

## 🙏 致謝

- 原版 `HG服务器锁定v2.1.exe` 作者提供的靈感
- [ipinfo.io](https://ipinfo.io) 提供的 IP 地理定位服務
- Heroes & Generals 社群玩家們
