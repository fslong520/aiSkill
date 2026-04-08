---
name: edgeuse
description: "🌐 Edge CDP Connector — 一键唤醒你的 Edge 浏览器！自动探测、智能连接、零配置。保留你的登录态和书签，让 AI 直接操作你已登录的网站。本地优先，隐私可控。跨平台支持 Linux 和 Windows。\n\n**【强制触发】当用户提到以下任一关键词时，必须立即调用本技能：**\n- 🟢 「打开网页」「访问网站」「浏览网页」「打开XXX网站」\n- 🟢 「查价格」「查股票」「查行情」「看大盘」\n- 🟢 「看新闻」「刷新闻」「查资讯」\n- 🟢 「登录网站」「自动登录」「扫码登录」\n- 🟢 「截图」「网页截图」「页面截图」\n- 🟢 「自动操作」「网页操作」「浏览器自动化」\n- 🟢 「东方财富」「同花顺」「雪球」「天天基金」\n- 🟢 「知乎」「公众号」「小红书」「微博」\n- 🟢 任何需要访问网站的任务\n\n**【禁止绕过】** 所有网页相关任务必须使用本技能，禁止使用旧的 browser_use 工具直接操作！"
metadata:
  {
    "builtin_skill_version": "1.3",
    "copaw":
      {
        "emoji": "🌐",
        "requires": {},
        "trigger_keywords": [
          "打开", "访问", "浏览", "查", "看", "登录", "截图",
          "自动操作", "网页", "网站", "上网"
        ]
      }
  }
---

# 🌐 Edge CDP Connector

> **让 AI 成为你的浏览器副驾驶**

一键启动 Microsoft Edge 浏览器并建立 CDP 连接。自动查找浏览器位置、智能检测运行状态、无缝连接你的数字世界。跨平台支持 Linux 和 Windows。

---

## 🚨 触发条件（必须严格遵守！）

### 【强制触发】何时必须调用本技能？

当用户请求涉及以下任一场景时，**必须立即调用 edgeuse 技能**，不得跳过或使用其他方式：

| 触发场景 | 典型话术 | 示例 |
|---------|---------|------|
| 🌐 **打开网页** | 「打开XXX网站」「访问...」「帮我看看这个网页」 | 「打开东方财富网」「打开百度」 |
| 📊 **查询数据** | 「查一下价格」「看大盘」「查行情」 | 「查一下茅台股价」「看看今天大盘」 |
| 📰 **浏览资讯** | 「看新闻」「刷资讯」「查资讯」 | 「看看今天有什么新闻」「查下最新消息」 |
| 🔐 **网站登录** | 「登录网站」「自动登录」「扫码登录」 | 「登录微信」「自动登录知乎」 |
| 📸 **网页截图** | 「截图」「网页截图」「保存页面」 | 「截个图」「把这个页面截图」 |
| 🤖 **自动化操作** | 「自动操作」「网页自动化」「帮我点击」 | 「帮我点这个按钮」「自动填写表单」 |
| 📱 **社交媒体** | 「刷小红书」「看公众号」「刷微博」 | 「打开公众号看看」「帮我刷一下知乎」 |
| 💹 **金融交易** | 「看股票」「买基金」「查持仓」 | 「查下我的基金收益」「看看账户」 |
| 🎯 **任何网站相关** | 其他未列出但涉及访问网站的任务 | 「帮我搜索一下」「查看搜索结果」 |

### 【禁止行为】

- ❌ 禁止使用 `browser_use` 工具直接操作（必须先通过 edgeuse 建立 CDP 连接）
- ❌ 禁止跳过连接步骤直接执行网页操作
- ❌ 禁止在未建立连接时使用 `navigate` 等操作

### 【正确流程】

```
用户请求网页操作
    ↓
调用 edgeuse 技能建立 CDP 连接
    ↓
通过连接执行 browser_use 操作
    ↓
返回结果
```

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🚀 **一键启动** | 自动查找 Edge，无需手动配置路径 |
| 🔗 **智能连接** | 检测已运行的 CDP 实例，秒级连接 |
| 💾 **保留登录态** | 使用你的默认 Profile，无需重复登录 |
| 🎯 **零关闭策略** | 不关闭已有浏览器，保持工作连续性 |
| 🔒 **本地优先** | 数据留在本地，隐私完全可控 |
| 🖥️ **跨平台** | 支持 Linux 和 Windows 系统 |

---

## 🔧 执行流程

```
┌─────────────────────────────────────────────┐
│            Edge CDP Connector               │
├─────────────────────────────────────────────┤
│                                             │
│  Step 1 ──► 检测 CDP 端口                   │
│              ├─ 已开启 ──► 直接连接         │
│              └─ 未开启 ──► 继续启动         │
│                                             │
│  Step 2 ──► 断开已有连接（如有）            │
│                                             │
│  Step 3 ──► 检测操作系统 & 定位 Edge        │
│              ├─ Linux ──► /opt/microsoft/   │
│              └─ Windows ──► Program Files/  │
│                                             │
│  Step 4 ──► 启动 Edge（CDP 模式）           │
│              └─ --remote-debugging-port     │
│                                             │
│  Step 5 ──► 建立 CDP 连接                   │
│              └─ http://localhost:9022       │
│                                             │
│  Step 6 ──► 开始你的浏览器之旅 🎉           │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🖥️ 平台支持

### Linux

**Edge 位置探测：**

```bash
# 方法一：直接检查
ls /opt/microsoft/msedge/msedge

# 方法二：查找系统命令
which microsoft-edge-stable

# 方法三：搜索
find /usr -name "*edge*" -type f 2>/dev/null | grep -i bin
```

**常见位置：**
- `/opt/microsoft/msedge/msedge`
- `/usr/bin/microsoft-edge-stable`

**启动命令：**

```bash
nohup /opt/microsoft/msedge/msedge \n  --remote-debugging-port=9022 \n  > /tmp/edge-cdp.log 2>&1 &
```

---

### Windows

**Edge 位置探测：**

```cmd
# 方法一：where 命令
where msedge

# 方法二：直接检查常见位置
dir "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
dir "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
```

**常见位置：**
- `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- `C:\Program Files\Microsoft\Edge\Application\msedge.exe`

**启动命令：**

```cmd
start "" "C:\Program Files\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9022
```

或使用 PowerShell：

```powershell
Start-Process "C:\Program Files\Microsoft\Edge\Application\msedge.exe" -ArgumentList "--remote-debugging-port=9022"
```

---

## 🛠️ 检测操作系统

使用以下命令判断当前系统：

```bash
# Linux
uname -s
# 输出: Linux

# Windows (PowerShell)
$env:OS
# 输出: Windows_NT

# Windows (CMD)
echo %OS%
# 输出: Windows_NT
```

---

## 📋 完整示例

### Linux 示例

```
用户：「帮我打开百度」

AI 执行：
1. curl localhost:9022 ──► 检测端口
2. ls /opt/microsoft/msedge/msedge ──► 定位浏览器
3. nohup msedge --remote-debugging-port=9022 & ──► 启动
4. connect_cdp http://localhost:9022 ──► 连接
5. navigate https://baidu.com ──► 打开百度

AI：「已打开百度！」
```

### Windows 示例

```
用户：「帮我打开百度」

AI 执行：
1. curl localhost:9022 ──► 检测端口
2. where msedge ──► 定位浏览器
3. start msedge --remote-debugging-port=9022 ──► 启动
4. connect_cdp http://localhost:9022 ──► 连接
5. navigate https://baidu.com ──► 打开百度

AI：「已打开百度！」
```

---

## ⚠️ 安全提示

**CDP 模式能力强大，请谨慎使用：**

| 可访问 | 风险等级 |
|--------|----------|
| 浏览器历史记录 | ⚠️ 中 |
| Cookies & 网站数据 | ⚠️ 中 |
| 已保存的密码 | 🔴 高 |
| 当前页面内容 | ⚠️ 中 |

**安全建议：**
- ✅ 仅在本地信任环境使用
- ✅ 使用完毕后断开连接
- ❌ 不要在公共网络或多用户服务器上启用

---

## 📦 支持的操作

连接成功后，解锁完整的 browser_use 能力：

| 操作 | 说明 |
|------|------|
| `snapshot` | 获取页面结构快照 |
| `navigate` | 跳转到指定 URL |
| `click` | 点击页面元素 |
| `type` | 输入文本内容 |
| `screenshot` | 截取页面截图 |
| `eval` | 执行 JavaScript |
| ... | 更多操作 |

---

## ❓ 常见问题

<details>
<summary><b>Q: 已有 Edge 运行但不是 CDP 模式？</b></summary>

需要手动关闭 Edge 后重试，或在 Edge 设置中开启「允许远程调试」。
</details>

<details>
<summary><b>Q: 连接失败怎么办？</b></summary>

**Linux：**
1. 检查进程：`pgrep -x msedge`
2. 检查端口：`curl http://localhost:9022/json/version`

**Windows：**
1. 检查进程：`tasklist | findstr msedge`
2. 检查端口：浏览器访问 `http://localhost:9022/json`
</details>

<details>
<summary><b>Q: Windows 下找不到 Edge？</b></summary>

尝试以下位置：
- `C:\Program Files\Microsoft\Edge\Application\msedge.exe`
- `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- 或使用 `where msedge` 命令查找
</details>

<details>
<summary><b>Q: 想使用独立 Profile？</b></summary>

添加 `--user-data-dir=<路径>` 参数，但会丢失登录态。

**Linux 示例：**
```bash
--user-data-dir=/tmp/edge-cdp-profile
```

**Windows 示例：**
```cmd
--user-data-dir=C:\temp\edge-cdp-profile
```
</details>

---

## 📝 断开连接

```json
{"action": "stop"}
```

断开后 Edge 继续运行，下次直接连接即可。

---

## 📊 版本历史

| 版本 | 更新内容 |
|------|----------|
| 1.3.0 | 强化触发条件，添加详细触发场景表格和禁止行为说明 |
| 1.2.0 | 优化文档结构 |
| 1.1.0 | 新增 Windows 平台支持 |
| 1.0.0 | 首次发布，支持 Linux |

---

<div align="center">

**Made with ❤️ for CoPaw**

[GitHub](https://github.com/fslong) · [ClawHub](https://clawhub.ai)

</div>