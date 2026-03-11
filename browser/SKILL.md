---
name: browser
description: "使用 Selenium WebDriver 控制浏览器进行自动化操作。**支持复用已运行的浏览器**，避免重复启动。"
metadata:
  {
    "copaw":
      {
        "emoji": "🧪",
        "requires": {"python": ["selenium"]}
      }
  }
---

# Browser 浏览器自动化技能

使用 Selenium 控制浏览器，**默认复用已运行的浏览器实例**。

## ⚠️ 最重要的原则

**默认直接连接已有浏览器，只有连不上才关闭重启！**

```
尝试连接 → 成功 → 使用
          ↓
        失败 → 关闭重启 → 连接 → 使用
```

## 🚀 标准使用模板

```python
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import subprocess
import time

def get_browser():
    """获取浏览器实例，优先复用已有浏览器"""
    options = Options()
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    
    # 先尝试连接已有浏览器
    try:
        driver = webdriver.Edge(options=options)
        print("✅ 已连接到现有浏览器")
        return driver
    except Exception as e:
        print(f"⚠️ 连接失败: {e}")
        print("正在重启浏览器...")
        
        # 连接失败，关闭并重启
        subprocess.run(['pkill', '-9', '-f', 'msedge'], capture_output=True)
        time.sleep(2)
        
        subprocess.run([
            'microsoft-edge',
            '--remote-debugging-port=9222',
            '--user-data-dir=' + subprocess.os.path.expanduser('~/.config/microsoft-edge'),
            '--disable-gpu',
            '--no-sandbox'
        ], start_new_session=True)
        time.sleep(3)
        
        # 再次尝试连接
        driver = webdriver.Edge(options=options)
        print("✅ 已启动新浏览器并连接")
        return driver

# 使用
driver = get_browser()
driver.get("https://example.com")
html = driver.page_source

# 断开连接（不关闭浏览器！）
driver.service.process.terminate()
```

## ⚡ 快速使用（确定浏览器已运行）

如果确定浏览器已经在运行，可以直接：

```python
from selenium import webdriver
from selenium.webdriver.edge.options import Options

options = Options()
options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
driver = webdriver.Edge(options=options)

# 使用浏览器...
driver.get(url)
html = driver.page_source

# 断开连接（不关闭浏览器）
driver.service.process.terminate()
```

## 🔄 推荐工作流程

### 步骤1：连接浏览器获取页面
```python
driver = get_browser()  # 或直接连接
driver.get(url)  # AI 决定访问哪个 URL
html = driver.page_source  # 获取页面源码
driver.service.process.terminate()  # 断开连接
```

### 步骤2：AI 分析页面内容
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')
# AI 根据页面结构决定如何提取数据
```

### 步骤3：AI 处理数据并执行后续任务
- AI 决定下一步操作
- 可能需要继续访问其他页面
- 可能需要保存数据、生成文件等

## 📋 核心原则

1. **直接连接优先** - 默认尝试连接 127.0.0.1:9222
2. **连不上才重启** - 只有连接失败时才关闭重启 Edge
3. **不断开浏览器** - 用 `terminate()` 断开，不要用 `quit()`
4. **AI 做决策** - Python 只是操作工具，决策靠 AI

## 注意事项

- **端口**: 默认使用 9222 端口
- **断开**: 用 `driver.service.process.terminate()` 而不是 `driver.quit()`
- **Cloudflare**: 首次访问某些网站可能需要人工验证
- **保持登录**: 复用模式可以保持 cookies 和登录状态