#!/usr/bin/env python3
"""
CDP 工具集 - 截图、读取内容、执行脚本
用法:
  python cdp_tools.py screenshot <page_id> <output.png>
  python cdp_tools.py read <page_id>
  python cdp_tools.py eval <page_id> "<javascript>"

常用 JS 操作示例:
  输入文字: eval <page_id> "document.querySelector('#input').value = '文字'"
  点击元素: eval <page_id> "document.querySelector('#btn').click()"
  获取标题: eval <page_id> "document.title"
  获取 URL: eval <page_id> "window.location.href"
  滚动页面: eval <page_id> "window.scrollBy(0, 500)"
"""

# 检查依赖
def check_dependencies():
    try:
        import websockets
    except ImportError:
        print("❌ 缺少依赖: websockets")
        print("请运行: pip install websockets")
        sys.exit(1)

import sys
check_dependencies()

import json
import asyncio
import websockets

async def cdp_command(ws, method, params=None, cmd_id=1):
    """发送 CDP 命令并返回结果"""
    cmd = {"id": cmd_id, "method": method}
    if params:
        cmd["params"] = params
    await ws.send(json.dumps(cmd))
    return json.loads(await ws.recv())

async def screenshot(page_id, output_path):
    """截图"""
    ws_url = f"ws://localhost:9022/devtools/page/{page_id}"
    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        await cdp_command(ws, "Page.enable")
        result = await cdp_command(ws, "Page.captureScreenshot", {"format": "png"}, 2)

        if "result" in result and "data" in result["result"]:
            import base64
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(result["result"]["data"]))
            print(f"✅ 截图已保存: {output_path}")
        else:
            print(f"❌ 截图失败: {result}")

async def read_content(page_id):
    """读取页面 HTML"""
    ws_url = f"ws://localhost:9022/devtools/page/{page_id}"
    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        await cdp_command(ws, "DOM.enable")
        doc = await cdp_command(ws, "DOM.getDocument", None, 2)
        node_id = doc["result"]["root"]["nodeId"]
        html = await cdp_command(ws, "DOM.getOuterHTML", {"nodeId": node_id}, 3)
        print(html["result"]["outerHTML"])

async def eval_js(page_id, js_code):
    """执行 JavaScript"""
    ws_url = f"ws://localhost:9022/devtools/page/{page_id}"
    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        result = await cdp_command(ws, "Runtime.evaluate", {
            "expression": js_code,
            "returnByValue": True
        })
        if "result" in result and "result" in result["result"]:
            value = result["result"]["result"].get("value")
            if value is not None:
                if isinstance(value, (dict, list)):
                    print(json.dumps(value, ensure_ascii=False, indent=2))
                else:
                    print(json.dumps(value, ensure_ascii=False))
            else:
                print("null")
        else:
            print(f"❌ 执行失败: {result}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    page_id = sys.argv[2]

    if cmd == "screenshot" and len(sys.argv) >= 4:
        asyncio.run(screenshot(page_id, sys.argv[3]))
    elif cmd == "read":
        asyncio.run(read_content(page_id))
    elif cmd == "eval" and len(sys.argv) >= 4:
        asyncio.run(eval_js(page_id, sys.argv[3]))
    else:
        print(__doc__)
