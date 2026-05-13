# Contest Step 1: 取赛题表

## 目标

访比赛任务列表页，析题信息，创题面汇总文件。

## 步骤

1. urlgo 访比赛任务列表页
2. snapshot 取页面构
3. 析题表：题号、标、时限、内存
4. 创题面汇总文件：`{contest_id}.md`
5. 写入始标签：`<div class="water">`
6. 报用户："现 N 道题，始逐题译..."

## 工优先级

```
1. urlgo（先）
2. BrowserUse（urlgo 不可用）
3. WebFetch（前皆不可用）
```

## 题面汇总文件格

```markdown
<div class="water">

# {比赛名}

---

（后续题逐题追加写入）

</div>
```

## 下一步

成 → `contest/02-problem.md`

败 → 查 URL 或问用户
