# 02-download — 从GESP官网下载PDF

## 官网结构

GESP 真题解析页 URL 模式：
- 列表页：`https://gesp.ccf.org.cn/101/1010/10166.html`（固定）
- 各期页面：逐年更新，在列表页中查找对应链接

## 步骤

1. 加载 urlgo 技能
2. 启动 CDP 浏览器：`urlgo cdp http://localhost:9222`（或自动启动）
3. 打开 GESP 真题列表页：`urlgo goto https://gesp.ccf.org.cn/101/1010/10166.html`
4. 截图或提取 HTML，找目标考试（年/月/级别）的 PDF 链接
   - PDF 链接格式通常是 `/cms/api/news/downloadFile?id=` 或 `/101/attach/xxx.pdf`
5. 构造完整 URL（若为相对路径则补 `https://gesp.ccf.org.cn`）
6. wget 下载到目标路径：
   ```bash
   wget -O "{pdf_path}" "{pdf_url}"
   ```

## 验证

- [ ] 文件已下载：`ls -la {pdf_path}` > 0 字节
- [ ] 可用 `pdftotext -layout {pdf_path} /dev/null` 测试能否正常解析

## 注意事项

- 官网页面可能刷新改版，若结构变化请探查当前页面
- 三级试卷可能有流程图嵌入（图片），需留意
- 优先用 urlgo，不用 playwright 或 webfetch
