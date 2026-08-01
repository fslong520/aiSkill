# 安装指南

## 下载

官方下载页：https://offline.tldraw.com/
GitHub 发布页：https://github.com/tldraw/tldraw-offline/releases/latest

各平台构建：

| 平台 | 格式 | 架构 |
|------|------|------|
| macOS | Universal DMG | Apple Silicon + Intel |
| Windows | Installer (.exe) | x64 或 Arm64 |
| Linux | AppImage | x64 或 Arm64 |
| Linux | 包 (.deb) | x64 |

## macOS

```bash
# 下载 DMG，挂载，拖入 Applications
# 首次开时会提示"未识别的开发者"
# 系统设置 → 隐私与安全性 → 仍要打开
```

或：

```bash
brew install --cask tldraw-offline
```

**注**：homebrew cask 可能不是最新版。官网页下载最稳妥。

## Windows

**winget（推荐）：**

```powershell
winget install --id tldraw.tldraw-offline
```

**手动安装：**
下载 exe 安装包双击。可选 x64 或 Arm64 版。

## Linux

### AppImage

```bash
# 示例：x64
chmod +x tldraw-offline-linux-x86_64.AppImage
./tldraw-offline-linux-x86_64.AppImage

# 装到 ~/.local/bin 随取随用
mv tldraw-offline-linux-x86_64.AppImage ~/.local/bin/tldraw
chmod +x ~/.local/bin/tldraw
```

### Debian 系

```bash
sudo dpkg -i tldraw-offline_1.12.0_amd64.deb
```

### Arch 系（Manjaro）

AppImage 通用，无需额外依赖。建议放 `~/.local/bin`。

## 安装验证

启动后终端检查：

```bash
curl -s http://localhost:7236/readme
```

有响应即就绪。

## 配置文件路径

```
~/.config/tldraw/server.json
```

内含 `port`、`token`、`pid`、`startedAt`。技能依赖此文件获得 API 认证。
