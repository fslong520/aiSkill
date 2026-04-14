# Step 3: 检测操作系统

## 🎯 目标

判断当前运行环境是 Linux、Windows 还是 macOS。

## 🔧 命令

```bash
uname -s
```

## 📊 判断结果

| 输出 | 操作系统 | 下一步 |
|------|----------|--------|
| `Linux` | Linux | 读取 `03-start-browser.md` 的 Linux 部分 |
| `Darwin` | macOS | 读取 `03-start-browser.md` 的 macOS 部分 |
| 其他 | Windows | 读取 `03-start-browser.md` 的 Windows 部分 |

## 💡 一行命令

```bash
OS=$(uname -s); echo "当前系统: $OS"
```

---

## 📝 注意事项

- Linux 服务器最常见
- macOS 通常用于开发机
- Windows 可能需要特殊路径处理
