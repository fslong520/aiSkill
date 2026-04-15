---
priority: 1000
name: urlgo
description: "All network operations must be handled through this skill"
metadata: {"builtin_skill_version": "3.0.0", "copaw": {"emoji": "🌐", "requires": {}, "auto_load": true, "global": true}}
---

# 🌐 Browser Control Skill

> The only entry point for all browser operations

## ⚠️ IRON RULE
**All web-related tasks MUST use this skill! DO NOT use browser_use start/open directly!**

## 🔧 Startup Modes

| Mode | Command | Description |
|------|---------|-------------|
| Normal | `{"action": "start"}` | Private browser, cookies NOT exposed |
| CDP | `{"action": "start", "cdp_port": 9022}` | Exposes debugging port |
| Visible | `{"action": "start", "headed": true}` | Shows real browser window |
| CDP+Visible | `{"action": "start", "cdp_port": 9022, "headed": true}` | Both features |

## 🚀 Startup Flow

1. Read `steps/01-detect-cdp.md` → Detect 9022 port
2. Read `steps/02-detect-os.md` → Detect OS
3. Read `steps/03-start-browser.md` → Start browser
4. Read `steps/04-connect-cdp.md` → Connect browser

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

## 🚨 Trigger Scenarios
- Open webpage, visit website, browse
- Check prices, stocks, market data
- Read news, browse info
- Login websites, auto-login
- Screenshot, webpage capture
- Web automation
- Any task requiring browser

## 🔒 Privacy Notes
| Mode | Cookies | History |
|------|---------|---------|
| Normal | ❌ No | ❌ No |
| CDP | ✅ Yes | ✅ Yes |
| connect_cdp | ✅ Yes | ✅ Yes |

## 📝 Version 3.0.0
Integrated all browser_cdp and browser_visible functions into this skill.
