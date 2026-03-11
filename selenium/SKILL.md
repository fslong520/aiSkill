---
name: selenium
description: "使用 Selenium WebDriver 控制浏览器进行自动化操作，支持页面交互、元素定位、数据抓取等任务。**默认使用有头模式**，哥哥可以看到浏览器操作过程。"
metadata:
  {
    "copaw":
      {
        "emoji": "🧪",
        "requires": {"python": ["selenium"]}
      }
  }
---

# Selenium 浏览器自动化技能

使用 **Selenium WebDriver** 控制浏览器进行自动化操作。**默认使用有头模式（可见浏览器窗口）**，哥哥可以亲眼看到浏览器操作过程。适用于需要复杂交互、动态页面处理、多标签页管理、文件上传下载等场景。

## 何时使用

- 需要复杂的浏览器自动化操作（点击、输入、拖拽、滚动等）
- 需要处理动态加载的内容（AJAX、JavaScript 渲染）
- 需要多标签页/窗口管理
- 需要文件上传/下载操作
- 需要执行自定义 JavaScript 代码
- 需要处理 iframe、弹窗、Alert 等特殊元素
- 需要隐式/显式等待元素加载
- **需要看到浏览器操作过程（默认有头模式）**

## 核心功能

### 1. 初始化浏览器

**默认有头模式（可见浏览器窗口）**：

```python
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置 Edge 浏览器选项（默认有头模式）
options = Options()
# options.add_argument('--headless')  # 如果需要无头模式，取消这行注释
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

# 初始化 Edge driver
driver = webdriver.Edge(options=options)
driver.implicitly_wait(10)  # 隐式等待 10 秒
```

**使用 Chrome 浏览器**：

```python
from selenium.webdriver.chrome.options import Options as ChromeOptions

options = ChromeOptions()
# options.add_argument('--headless')  # 默认不使用无头模式
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
```

**无头模式（后台运行，不可见）**：

```python
options.add_argument('--headless')  # 添加此行启用无头模式
```

---

### 1.5 控制已打开的浏览器（复用当前会话）⭐

如果哥哥想**控制已经在运行的浏览器**（比如已经手动登录了网站），可以用这个方法：

#### 步骤 1：以调试模式启动浏览器

**⚠️ 重要：使用原有用户数据目录避免被判定为机器人**

如果哥哥想访问有 Cloudflare 防护的网站（如 Codeforces），**必须使用原有的用户数据目录**，而不是新建的空目录。原有目录包含 cookies、浏览历史，不会被判定为机器人。

**Edge 浏览器（Linux）- 使用原有配置**：
```bash
# 先关闭所有 Edge 进程
pkill -f microsoft-edge

# 以调试模式启动 Edge（使用原有用户数据目录）
microsoft-edge --remote-debugging-port=9222 \
               --user-data-dir="$HOME/.config/microsoft-edge" \
               --disable-gpu --no-sandbox
```

**Chrome 浏览器（Linux）- 使用原有配置**：
```bash
# 先关闭所有 Chrome 进程
pkill -f chrome

# 以调试模式启动 Chrome（使用原有用户数据目录）
google-chrome --remote-debugging-port=9222 \
              --user-data-dir="$HOME/.config/google-chrome" \
              --disable-gpu --no-sandbox
```

**Windows PowerShell**：
```powershell
# Edge（使用原有配置）
Start-Process "msedge" --args "--remote-debugging-port=9222", "--user-data-dir=$env:LOCALAPPDATA\Microsoft\Edge\User Data"

# Chrome（使用原有配置）
Start-Process "chrome" --args "--remote-debugging-port=9222", "--user-data-dir=$env:LOCALAPPDATA\Google\Chrome\User Data"
```

**为什么不使用新目录？**
- ❌ 新目录（如 `/tmp/edge-debug-profile`）：没有 cookies、没有浏览历史 → Cloudflare 判定为机器人
- ✅ 原有目录（如 `~/.config/microsoft-edge`）：包含登录状态、cookies → 正常访问

#### 步骤 2：Selenium 连接到调试端口

```python
from selenium import webdriver
from selenium.webdriver.edge.options import Options

options = Options()
options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')

# 连接到已打开的浏览器
driver = webdriver.Edge(options=options)

# 现在可以控制已经打开的浏览器了！
print(f"当前页面：{driver.title}")
print(f"当前 URL: {driver.current_url}")

# 进行操作
driver.get('https://codeforces.com')
# ... 继续操作

driver.quit()  # 注意：这会关闭浏览器！
```

#### 步骤 3：不关闭浏览器（可选）

如果不想让 `driver.quit()` 关闭浏览器，可以：

```python
# 不调用 quit()，只关闭连接
driver.service.process.terminate()
```

#### 注意事项

⚠️ **重要提示**：
1. 必须先**完全关闭**同类型浏览器，再以调试模式启动
2. `--user-data-dir` 必须指向**原有的用户数据目录**（不是新目录！）
   - Linux Edge: `~/.config/microsoft-edge`
   - Linux Chrome: `~/.config/google-chrome`
   - Windows Edge: `%LOCALAPPDATA%\Microsoft\Edge\User Data`
   - Windows Chrome: `%LOCALAPPDATA%\Google\Chrome\User Data`
3. 调试模式下浏览器会有安全警告，这是正常的
4. `driver.quit()` 会**关闭整个浏览器**，如果不想关闭，只终止 service
5. 调试端口（默认 9222）不能被其他程序占用
6. **关键区别**：
   - 新目录 → Cloudflare 验证失败（被判定为机器人）
   - 原有目录 → 正常访问（复用已有 cookies）

#### 完整示例：控制现有浏览器

```python
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

# 连接到调试端口
options = Options()
options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')

try:
    driver = webdriver.Edge(options=options)
    print(f"✓ 已连接到浏览器")
    print(f"当前页面：{driver.title}")
    
    # 在已打开的浏览器中操作
    driver.get('https://codeforces.com/problemset/problem/677/A')
    time.sleep(3)
    
    # 获取页面内容
    html = driver.page_source
    print(f"页面长度：{len(html)}")
    
    # 截图
    driver.save_screenshot('/tmp/current_browser.png')
    print("✓ 已保存截图")
    
    # 不关闭浏览器，只断开连接
    driver.service.process.terminate()
    print("✓ 已断开连接，浏览器保持打开")
    
except Exception as e:
    print(f"错误：{e}")
    print("请确保浏览器已以调试模式启动")
```

#### 一键启动脚本

创建一个脚本快速启动调试模式浏览器：

```bash
#!/bin/bash
# start_debug_browser.sh

# 关闭现有浏览器
pkill -f microsoft-edge

# 创建调试配置目录
mkdir -p /tmp/edge-debug-profile

# 启动调试模式 Edge
microsoft-edge --remote-debugging-port=9222 \
               --user-data-dir=/tmp/edge-debug-profile \
               --disable-gpu \
               --no-sandbox &

echo "✓ Edge 已以调试模式启动"
echo "✓ 现在可以用 Selenium 连接到 127.0.0.1:9222"
```

使用方法：
```bash
chmod +x start_debug_browser.sh
./start_debug_browser.sh
```

### 2. 打开页面

```python
driver.get('https://example.com')
driver.maximize_window()
```

### 3. 元素定位

```python
# 多种定位方式
element = driver.find_element(By.ID, 'element_id')
element = driver.find_element(By.NAME, 'element_name')
element = driver.find_element(By.CLASS_NAME, 'class_name')
element = driver.find_element(By.XPATH, '//div[@class="example"]')
element = driver.find_element(By.CSS_SELECTOR, 'div.example')
element = driver.find_element(By.LINK_TEXT, '链接文本')
element = driver.find_element(By.PARTIAL_LINK_TEXT, '部分链接')
element = driver.find_element(By.TAG_NAME, 'div')

# 查找多个元素
elements = driver.find_elements(By.CLASS_NAME, 'item')
```

### 4. 元素操作

```python
# 点击
element.click()

# 输入文本
input_field.send_keys('要输入的文本')
input_field.clear()  # 清空

# 提交表单
element.submit()

# 获取文本
text = element.text
value = element.get_attribute('value')

# 获取属性
href = element.get_attribute('href')
class_name = element.get_attribute('class')

# 判断元素状态
is_displayed = element.is_displayed()
is_enabled = element.is_enabled()
is_selected = element.is_selected()
```

### 5. 等待机制

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 显式等待 - 等待元素可见
wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.ID, 'myElement')))

# 等待元素可点击
element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.submit')))

# 等待元素出现
element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="content"]')))

# 等待文本出现
wait.until(lambda d: 'expected text' in d.page_source)

# 等待 URL 变化
wait.until(EC.url_contains('/dashboard'))
```

### 6. 执行 JavaScript

```python
# 执行脚本
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

# 带参数的脚本
driver.execute_script('arguments[0].click();', element)

# 获取返回值
title = driver.execute_script('return document.title;')
```

### 7. 处理 iframe

```python
# 切换到 iframe
driver.switch_to.frame('iframe_id')
driver.switch_to.frame(0)  # 按索引
driver.switch_to.frame(element)  # 按元素

# 切回主文档
driver.switch_to.default_content()

# 切换到父 iframe
driver.switch_to.parent_frame()
```

### 8. 处理弹窗/Alert

```python
from selenium.webdriver.common.alert import Alert

# 切换到 alert
alert = driver.switch_to.alert

# 获取文本
alert_text = alert.text

# 接受（确定）
alert.accept()

# dismiss（取消）
alert.dismiss()

# 输入（prompt 弹窗）
alert.send_keys('输入内容')
```

### 9. 多标签页/窗口管理

```python
# 获取当前窗口句柄
current_window = driver.current_window_handle

# 获取所有窗口句柄
all_windows = driver.window_handles

# 切换到新窗口
for window in driver.window_handles:
    if window != current_window:
        driver.switch_to.window(window)
        break

# 按标题切换
driver.switch_to.window('window_title')

# 打开新标签页
driver.execute_script('window.open("https://example.com", "_blank");')

# 关闭窗口
driver.close()
```

### 10. 文件上传

```python
# 找到文件输入框并上传
upload_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
upload_input.send_keys('/absolute/path/to/file.txt')
```

### 11. 文件下载配置

```python
# 配置下载目录
prefs = {
    'download.default_directory': '/path/to/download/dir',
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
}
options.add_experimental_option('prefs', prefs)
```

### 12. 截图

```python
# 截取整个页面
driver.save_screenshot('/path/to/screenshot.png')

# 截取元素截图（需要额外库）
# element.screenshot('/path/to/element.png')
```

### 13. Cookies 管理

```python
# 获取所有 cookies
cookies = driver.get_cookies()

# 添加 cookie
driver.add_cookie({'name': 'session', 'value': 'abc123'})

# 删除指定 cookie
driver.delete_cookie('session')

# 删除所有 cookies
driver.delete_all_cookies()
```

### 14. 关闭浏览器

```python
driver.quit()  # 关闭所有窗口并结束会话
# driver.close()  # 仅关闭当前窗口
```

## 完整示例

### 示例 1：使用 Edge 浏览器抓取数据（有头模式）

```python
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_with_edge():
    # 默认有头模式，哥哥可以看到浏览器
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Edge(options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # 打开页面
        driver.get('https://codeforces.com/problemset/problem/677/A')
        
        # 等待页面加载（处理 Cloudflare 验证）
        wait.until(lambda d: 'problem-statement' in d.page_source)
        
        # 获取页面内容
        html = driver.page_source
        print(f"页面长度：{len(html)}")
        
        # 截图
        driver.save_screenshot('/tmp/screenshot.png')
        
        return html
    finally:
        driver.quit()
```

### 示例 2：登录并抓取数据

### 示例 2：处理动态加载内容（有头模式）

```python
import time
from selenium.webdriver.edge.options import Options

def scrape_infinite_scroll():
    # 有头模式，可以看到滚动过程
    options = Options()
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Edge(options=options)
    driver.get('https://example.com/infinite')
    
    last_height = driver.execute_script('return document.body.scrollHeight')
    
    while True:
        # 滚动到底部（可以看到动画效果）
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        
        # 等待新内容加载
        time.sleep(2)
        
        # 检查是否还有新内容
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
    
    items = driver.find_elements(By.CLASS_NAME, 'item')
    driver.quit()
```

## 常见异常处理

```python
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException
)

try:
    element = driver.find_element(By.ID, 'not_exist')
except NoSuchElementException:
    print('元素不存在')

try:
    wait.until(EC.presence_of_element_located((By.ID, 'timeout')), timeout=5)
except TimeoutException:
    print('等待超时')

# 处理元素被遮挡
try:
    element.click()
except ElementClickInterceptedException:
    driver.execute_script('arguments[0].click();', element)

# 处理元素过期
try:
    text = element.text
except StaleElementReferenceException:
    element = driver.find_element(By.ID, 'id')  # 重新查找
    text = element.text
```

## 最佳实践

1. **优先使用显式等待**，而不是 time.sleep()
2. **使用 try-finally** 确保 driver.quit() 被执行
3. **选择稳定的定位方式**：ID > Name > CSS Selector > XPath
4. **避免硬编码等待时间**，使用 WebDriverWait
5. **处理 iframe 后记得切回** default_content()
6. **默认使用有头模式**，可以看到操作过程，调试更方便
7. **设置合理的超时时间**，避免无限等待
8. **捕获并处理异常**，提高脚本健壮性
9. **处理 Cloudflare 验证**：使用 `wait.until()` 等待页面元素出现

## 注意事项

- ✅ **默认有头模式**：哥哥可以看到浏览器操作过程
- ✅ **Edge/Chrome 都支持**：根据需要选择浏览器
- ✅ **无头模式可选**：添加 `--headless` 参数即可启用
- 确保已安装 selenium：`pip install selenium`
- 需要对应的 WebDriver（EdgeDriver 或 ChromeDriver）
- 频繁请求可能被反爬，适当添加延迟
- 遵守目标网站的 robots.txt 和使用条款
- 有 Cloudflare 防护的网站需要等待验证通过
