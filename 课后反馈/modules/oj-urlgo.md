# 课后反馈 - urlgo 页面操作细节

> 今日实战验证（2026-08-09，ZGOJ）。所有命令基于 `python3 /home/fslong/.config/opencode/skills/urlgo/urlgo`。

## 1. 浏览器启动

```bash
python3 /home/fslong/.config/opencode/skills/urlgo/urlgo status   # 查 CDP
python3 /home/fslong/.config/opencode/skills/urlgo/urlgo start    # 起浏览器
```

**踩坑：edge 正在使用 → start 失败**（提示"请先关闭现有 edge"）。
用户浏览器不可杀。改用 chromium 手动起 CDP（独立 user-data-dir，不动 edge）：

```bash
nohup chromium --remote-debugging-port=9022 --no-first-run --user-data-dir=/tmp/urlgo-chromium >/dev/null 2>&1 &
sleep 3
python3 /home/fslong/.config/opencode/skills/urlgo/urlgo status   # ✅ CDP 已开启
```

## 2. 打开状态页

```bash
python3 /home/fslong/.config/opencode/skills/urlgo/urlgo open "https://{OJ}/status?onlyMine=false&username={用户名}&currentPage=1&limit=15"
```

**⚠️ 每次 open 返回新页面 ID**（如 `B15C489F...`），后续所有操作**必须用新 ID**，不用旧的。

**踩坑：URL 的 username 参数常不生效**——打开后列表仍是全部提交，必须页面筛选（见下）。

## 3. 筛选作者（逐字符触发 Vue）

**踩坑：直接 `input.value='xx'` 不触发 Vue**，须逐字符 + 派发 input 事件 + Enter：

```js
const input = document.querySelector('input[placeholder="请输入作者"]');
input.focus();
const text = '用户名';
input.value = '';
for(let c of text) { input.value += c; input.dispatchEvent(new Event('input', {bubbles: true})); }
input.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', keyCode: 13, bubbles: true}));
input.dispatchEvent(new KeyboardEvent('keyup', {key: 'Enter', keyCode: 13, bubbles: true}));
```

执行：`urlgo eval {ID} "{上面JS}"` → sleep 3 → 验证列表。

## 4. 提取提交记录表

```js
var rows=document.querySelectorAll('.vxe-body--row');
var out=[];
for(var i=0;i<rows.length;i++){
  var tds=rows[i].querySelectorAll('td');
  out.push({id:tds[0].textContent.trim(), problem:tds[1].textContent.trim(),
            status:tds[2].textContent.trim(), score:tds[3].textContent.trim(),
            lang:tds[7].textContent.trim(), author:tds[9].textContent.trim(),
            time:tds[10].textContent.trim()});
}
JSON.stringify(out);
```

**列索引**（ZGOJ，0 起）：

| 索引 | 内容 |
|:---:|------|
| 0 | Run ID |
| 1 | 题目 |
| 2 | 状态（含隐藏弹窗文字，取前 15 字） |
| 3 | 分数 |
| 4 | 运行时间 |
| 5 | 内存 |
| 6 | 代码长度 |
| 7 | 语言 |
| 8 | 判题源 |
| 9 | 作者 |
| 10 | 提交时间 |
| 11 | 操作 |

## 5. 进提交详情（关键）

**踩坑：点行、点 Run ID、双击都无效**。唯一入口 = 点该行**语言列**的 span：

```js
var rows=document.querySelectorAll('.vxe-body--row');
var target=null;
for(var i=0;i<rows.length;i++){
  var tds=rows[i].querySelectorAll('td');
  if(tds[0].textContent.trim()==='{目标RunID}'){target=rows[i];break;}
}
if(target){ var td=target.querySelector('td.col_9 span'); td.click(); 'clicked-{目标RunID}'; }
else { 'not-found'; }
```

跳转后页面 URL 变为 `{OJ}/submission-detail/{id}`（同一 ID 页内导航，无需重新 open）。

## 6. 取代码

```js
document.body.innerText.match(/include[\s\S]*复制/)?.[0] || 'no-code'
```

返回从 `#include` 到"复制"按钮的完整代码文本。

## 7. 切换学生

`urlgo open` 新状态页（新用户名）→ 重复 2-6。每学生独立循环：筛选 → 列表 → 逐题详情。

## 多题批量

同一学生的列表页可循环点多个 Run ID 的语言列（每点一个取一次代码），不必反复 open。

## AVOID

- AVOID 杀用户正在用的 edge（改用 chromium 独立实例）
- AVOID 用旧页面 ID（open 后必须换新 ID）
- AVOID 相信 URL username 参数已筛选
- AVOID 点行/双击进详情（只有语言列可点）
- AVOID 用 snapshot 读代码（含大量无关文本，用 innerText.match）
