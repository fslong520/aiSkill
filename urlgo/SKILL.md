---
priority: 1000
name: urlgo
description: "All network operations must be handled through this skill"
metadata: {"builtin_skill_version": "3.1.0", "copaw": {"emoji": "🌐", "requires": {}, "auto_load": true, "global": true}}
---

# 🌐 Browser Control Skill

> The only entry point for all browser operations

## ⚠️ IRON RULE
**All web-related tasks MUST use this skill! DO NOT use browser_use start/open directly!**

## ⚠️ 按需读取铁律
**SKILL.md 只是入口！不要一次性读取所有步骤文档！**
1. 先读 SKILL.md 确定入口步骤
2. 按入口指引读取对应 step 文档
3. step 文档读完后根据结果决定跳转到哪个 step
4. **一步一步读，不要批量读取！**

---

## 🚀 启动流程入口

**第一步：读取 `steps/01-detect-cdp.md`**

该文档会告诉你：
- 如何检测 9022 端口状态
- 根据检测结果决定下一步跳转到哪个 step

**流程图**：
```
入口: 读取 steps/01-detect-cdp.md
         ↓
    检测 9022 端口
         ↓
    ┌────┴────┐
    ↓         ↓
 已开启     未开启
    ↓         ↓
 Step 4    Step 2 → Step 3 → Step 4
(连接)    (检测OS) (启动)   (连接)
```

---

## 🔧 Startup Modes

| Mode | Command | Description |
|------|---------|-------------|
| Normal | `{"action": "start"}` | Private browser, cookies NOT exposed |
| CDP | `{"action": "start", "cdp_port": 9022}` | Exposes debugging port |
| Visible | `{"action": "start", "headed": true}` | Shows real browser window |
| CDP+Visible | `{"action": "start", "cdp_port": 9022, "headed": true}` | Both features |

---

## 🎯 All browser_use Actions

### Startup & Connection
| Action | Description |
|--------|-------------|
| `start` | Start browser |
| `start cdp_port` | Start with CDP exposed |
| `start headed` | Start visible browser |
| `connect_cdp` | Connect to existing browser |
| `list_cdp_targets` | Scan CDP ports |
| `stop` | Stop/disconnect |

### Page Operations
| Action | Description |
|--------|-------------|
| `open` | Open URL in new tab |
| `navigate` | Navigate in current page |
| `navigate_back` | Go back |

### Content Retrieval
| Action | Description |
|--------|-------------|
| `snapshot` | Get page DOM structure |
| `screenshot` | Take screenshot |
| `console_messages` | Get console logs |
| `network_requests` | Get network requests |

### Interaction
| Action | Description |
|--------|-------------|
| `click` | Click element |
| `type` | Type text |
| `fill_form` | Fill form fields |
| `select_option` | Select dropdown |
| `hover` | Hover element |
| `drag` | Drag element |
| `press_key` | Press keyboard key |

### Special Operations
| Action | Description |
|--------|-------------|
| `evaluate` | Execute JavaScript |
| `run_code` | Run code |
| `wait_for` | Wait for condition |
| `handle_dialog` | Handle dialogs |
| `file_upload` | Upload files |

### Browser Management
| Action | Description |
|--------|-------------|
| `tabs` | Manage tabs |
| `resize` | Resize window |
| `pdf` | Export PDF |
| `clear_browser_cache` | Clear cache |
| `cookies_get/set/clear` | Cookie operations |

---

## 🚨 Trigger Scenarios
- Open webpage, visit website, browse
- Check prices, stocks, market data
- Read news, browse info
- Login websites, auto-login
- Screenshot, webpage capture
- Web automation
- Any task requiring browser

---

## 🔒 Privacy Notes
| Mode | Cookies | History |
|------|---------|---------|
| Normal | ❌ No | ❌ No |
| CDP | ✅ Yes | ✅ Yes |
| connect_cdp | ✅ Yes | ✅ Yes |

---

## 📝 Version 3.1.0
改进：按步骤入口、按需读取，避免一次性读取所有文档导致上下文膨胀