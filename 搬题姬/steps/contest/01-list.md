# Contest Step 1: 获取比赛题目列表

## 目标

访问比赛任务列表页，解析题目信息，创建题面汇总文件。

## 步骤

1. urlgo 访问比赛任务列表页
2. snapshot 获取页面结构
3. 解析题目列表：题号、标题、时限、内存
4. 创建题面汇总文件：`{contest_id}.md`
5. 写入开始标签：`<div class="water">`
6. 报告用户："发现 N 道题目，开始逐题翻译..."

## 题面汇总文件格式

```markdown
<div class="water">

# {比赛名称}

---

（后续题目逐题追加写入）

</div>
```

## 下一步

成功 → `contest/02-problem.md`

失败 → 检查 URL 或询问用户
