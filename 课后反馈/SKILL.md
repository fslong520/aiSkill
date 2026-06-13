---
name: 课后反馈
description: 使用urlgo技能操作OJ网页，查看学生提交代码，生成课后反馈报告
allowed-tools:
  - bash
  - Read
  - Write
  - Edit
  - AskUserQuestion

metadata:
  slug: class-feedback
  trigger: 课后反馈、课后总结、学生表现、课堂反馈

---

## Keywords

课后反馈, 学生表现, 代码分析, OJ提交, 课堂评价

## Summary

使用urlgo技能操作OJ网页，查看学生提交代码，生成课后反馈报告。**必须使用urlgo技能操作网页，禁止自行拼接地址**。

## Strategy

1. 使用urlgo打开OJ状态页面
2. 使用urlgo筛选学生提交记录
3. 使用urlgo点击进入每条提交详情
4. 使用urlgo查看学生代码
5. 生成课后反馈报告

## ⚠️ 核心原则（必须遵守）

**所有网页操作必须通过urlgo技能完成，禁止：**
- ❌ 自行拼接URL地址
- ❌ 使用curl/webfetch直接访问
- ❌ 使用edgeuse/browser_use

**正确做法：**
- ✅ 每一步都用urlgo打开页面
- ✅ 每一步都用urlgo点击元素
- ✅ 每一步都用urlgo执行JS
- ✅ 从页面中获取真实链接，不自己构造

## 核心配置

| 配置项 | 来源 |
|-------|-----|
| OJ地址 | **用户必须提供** |
| 学生用户名 | **用户必须提供** |
| 课程内容 | **用户必须提供** |
| 输出目录 | 用户指定或当前目录 |

---

## 工作流程

### Step 1: 获取OJ地址和学生信息

询问用户：
1. **OJ地址**（必须询问，不要假设）
2. 学生姓名/用户名列表
3. 要查看的题目范围（今天/本周/某节课）

**示例对话：**
```
请提供OJ地址：（用户输入）
请输入学生用户名：（用户输入）
今天上了什么课：（用户输入）
```

### Step 2: 打开OJ状态页面

**必须使用urlgo打开页面（使用用户提供的OJ地址）：**

```bash
# 调用urlgo技能
skill name="urlgo" user_message="start"
skill name="urlgo" user_message="open url=${用户提供的OJ地址}/status"
```

### Step 3: 筛选学生提交

**使用urlgo执行JS筛选学生：**

```bash
# 调用urlgo技能执行JS
skill name="urlgo" user_message="exec_js js=JSON.stringify({rows: window._vxe_table_component?.getData()?.length})"
```

**使用urlgo筛选学生（逐字符输入触发Vue响应）：**

```bash
# 调用urlgo技能获取筛选输入框
skill name="urlgo" user_message="exec_js js=document.querySelector('input[placeholder=\"请输入作者\"]')?.className"
```

**逐字符输入筛选条件：**
```bash
# 调用urlgo技能对每个字符执行input事件（将 ${用户名} 替换为实际用户名）
skill name="urlgo" user_message="exec_js js=const input = document.querySelector('input[placeholder=\"请输入作者\"]'); input.focus(); const text = '${用户名}'; for(let c of text) { input.value += c; input.dispatchEvent(new Event('input', {bubbles: true)); }"
```

### Step 4: 获取提交记录

**从页面表格中提取数据：**

```bash
# 调用urlgo技能获取提交记录
skill name="urlgo" user_message="exec_js js=const rows = document.querySelectorAll('.vxe-body--row'); const data = []; rows.forEach(row => { const cells = row.querySelectorAll('.vxe-body--column'); if(cells.length > 0) { data.push({ submitId: cells[0]?.textContent?.trim(), problem: cells[1]?.textContent?.trim(), user: cells[3]?.textContent?.trim(), status: cells[4]?.textContent?.trim(), time: cells[7]?.textContent?.trim() }); } }); JSON.stringify(data);"
```

**⚠️ 重要：submitId必须从页面获取，不要自行构造！**

### Step 5: 查看学生代码

**使用urlgo点击进入提交详情：**

```bash
# 调用urlgo技能找到提交ID对应的链接
skill name="urlgo" user_message="exec_js js=const links = document.querySelectorAll('a[href*=\"submission-detail\"]'); Array.from(links).map(l => l.href);"
```

**使用urlgo打开提交详情页面：**

```bash
# 调用urlgo技能使用从页面获取的真实链接
skill name="urlgo" user_message="open url=从上面获取的真实链接"
```

**使用urlgo获取代码内容：**

```bash
# 调用urlgo技能获取代码
skill name="urlgo" user_message="exec_js js=document.querySelector('pre')?.textContent || document.querySelector('code')?.textContent || '代码未找到';"
```

### Step 6: 生成课后反馈

基于收集到的代码，生成课后反馈报告。

**报告格式：**

```markdown
本次课我们学习的是《XXX》，这次课的教学目的有：

1. **教学目的1**
2. **教学目的2**

## 一、重点知识

### 1. 知识点1
纯知识点讲解和代码示例，不掺杂任何评价

### 2. 知识点2
纯知识点讲解和代码示例，不掺杂任何评价

## 二、上课情况

### **1. 表现情况**

- 本次课我们学习了XXX，同学们的表现整体不错：
  - **学生1**：一两句话评价
  - **学生2**：一两句话评价

### **2. 课堂评价**

| 姓名       | 作业 | 注意力 | 代码力 | 创造力 | 思维力 |
|------------|------|--------|--------|--------|--------|
| **学生1** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## 三、课后作业

1. 作业1
2. 作业2
```

**⚠️ 知识点与评价分离原则：**
- **一、重点知识**：只讲知识点，不出现学生代码对比，不出现评价性内容
- **二、上课情况**：只做评价，不重复知识点
- **评价要基于实际代码**：必须用urlgo查看学生代码后才能写评价

---

## ⚠️ 常见错误（必须避免）

| 错误 | 正确做法 |
|------|---------|
| 自行拼接submission-detail/submitId | 从页面表格中获取submitId，使用urlgo点击进入 |
| 用curl访问OJ API | 使用urlgo操作网页，Vue SPA的API需要登录态 |
| 不看代码就写评价 | 必须用urlgo查看每个学生的实际代码 |
| 只看第一页 | 使用urlgo翻页直到超出时间范围 |
| 评价泛泛而谈 | 基于实际代码分析，指出具体优点和问题 |
| 知识点部分放学生代码 | 知识点只讲知识点，不出现学生代码对比 |
| 知识点部分掺杂评价 | "四位同学都正确实现了"这种话不能出现在知识点部分 |

---

## urlgo命令参考

```bash
# 启动浏览器
skill name="urlgo" user_message="start"

# 打开页面
skill name="urlgo" user_message="open url=URL"

# 执行JS
skill name="urlgo" user_message="exec_js js=JS代码"

# 截图
skill name="urlgo" user_message="screenshot"

# 关闭浏览器
skill name="urlgo" user_message="stop"
```

---

## 质量检查

- [ ] 使用urlgo打开OJ状态页面
- [ ] 使用urlgo筛选学生提交记录
- [ ] 使用urlgo点击进入每条提交详情
- [ ] 使用urlgo查看学生实际代码
- [ ] 重点知识只讲知识点，不掺杂评价
- [ ] 重点知识不出现学生代码对比
- [ ] 上课情况基于实际代码分析，指出具体优缺点
- [ ] 评价简洁（每个学生一两句话）
- [ ] 禁止自行拼接任何URL地址
