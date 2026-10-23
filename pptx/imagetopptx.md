# Image-to-Editable-PPTX（图片复刻为可编辑 PPT）

> 融合自 knight-imagetopptx-skill（MIT, github.com/knight6669/knight-imagetopptx-skill），适配 Linux + 本地技能栈。
> 与上游差异：上游「Non-Negotiable Image-Generation Gate」禁止脚本绘制一切图标，理由是保真；本地版经哥哥决策放开——**简单几何图标优先 SVG 直绘**（确定性控色控形，优于生图抽卡），复杂视觉仍走生图。
> 适用：把一张幻灯片图片 / 截图 / 纯图片页 PPTX / PDF 页 / AI 生成的整页图，重建为**元素可编辑**的 .pptx。
> 不适用：从零创作新 deck（用 pptxgenjs.md）、或仅把图片贴进幻灯片（无需对象级编辑时直接 addImage）。

## 核心原则：语义重建，分类处理

- **文本、卡片、面板、分隔线、普通箭头、徽章、表格** → 一律原生 PowerPoint 对象（可编辑）。
- **简单几何图标（对勾/齿轮/箭头组合/几何 logo/单色 pictogram）** → **优先手绘 SVG** 再转透明 PNG：色值精确到 hex、矢量无损、改色即改代码，比生图可控。复杂插画才走生图。
- **插画、吉祥物、复杂徽章、流程缎带箭头（ribbon/multi-lane/渐变箭头带）、照片级元素** → AI 生成或素材库透明 PNG，插入 PPT 后置于原生对象之上。
- 参考图裁剪片段只作参照，不作最终图标资产（除非用户要求保留精确 logo）。

## 工作流（按序执行，写 compact 执行报告）

1. **准备**：建工作目录 `editable-replica-XX/`；纯图片 PPTX/PDF 先逐页渲染为 PNG（soffice→pdftoppm，见主 SKILL.md）；记录每页尺寸/宽高比，按源图比例选幻灯片尺寸（如 1536×1024 源 → 12×8 in = 128px/in 干净映射）。
2. **盘点**：列出标题/正文/卡片/箭头/图标/表格，赋稳定 ID（如 `process_log_parse`），记录近似 bbox。每个非文本区域二分类：`native_editable` 或 `image_asset`。
3. **资产制备**（image_asset 类）：
   - **SVG 直绘优先**（简单几何图标）：手写 SVG（精确 hex 色、`viewBox` 归一、纯路径），cairosvg 转 RGBA 透明 PNG——`python3 -c "import cairosvg; cairosvg.svg2png(bytestring=svg.encode(), write_to='icon.png', output_width=W, output_height=W)"`。**以 2x 目标尺寸输出**（PPT 内按可见尺寸缩回，抗糊）。依赖 `pip install cairosvg`（本机已装）。背景须真透明（禁白底矩形），线帽/拐角用 `stroke-linecap/linejoin="round"` 近似圆角笔触。
   - 图标类（复杂）：找风格匹配的透明 PNG 素材或由生图模型生成；**色彩忠实第一关**——prompt/选材前先采样参考色（前景描边/填充/容器色/单色/白底彩/彩底白），逐资产记录 hex，不靠后处理调色补救。
   - 网格图切分：仅当确有 C×R 对齐规则时用网格生成；先做 alpha 内容检测（前景投影找 C 列 R 行中心，从中心中点切，不从 (0,0) 均分），检测数不符即判废重生。
   - 切后逐格验：RGBA 模式、四角透明、alpha bbox 非空、无跨格残渣（邻格弧线/圆点/楔形即废）；用 `check_rebuild_assets.py` 校验透明边距 ≥10px。
   - 居中归一：按 alpha 质心（非 bbox 中心）重新装进方形透明画布并留边——不对称图标（星/靶/人像光芒/放大镜）bbox 居中会偏。
   - 复杂视觉（缎带箭头/迁移流/插画区）：生成时定死车道数、方向、色角色、渐隐、曲率、箭头头部样式；只按语义区域切分（如左流/右流两条），不按每条 lane 碎切。
4. **重建**（python-pptx 或 pptxgenjs）：
   - 纯白/米白底用 slide 背景填充，不铺全页白矩形（选择窗格干净）。
   - 全部可读文本用原生文本框，禁光栅化。
   - **箭头几何先行**：厚实填充箭头（卡间流程步）用原生 `DOWN_ARROW` 等填充形，非细线连接符；细线才用 connector。U 形/回环/钩形箭头：内置 U-turn 形先在 0/90/180/270 四旋转中选，不匹配则用单条可编辑 freeform 弧线+原生箭头；禁用多段直线拼弧。方向敏感形（漏斗/梯形/chevron）先渲染比对方向，防默认朝向反了。
   - 圆角矩形显式设 `shape.adjustments[0]`：大面板 0.025–0.04，胶囊/按钮 0.06–0.10（默认值在某些宽高比下变超大胶囊）。
   - 图标插入按 alpha 可见范围缩放、质心对目标槽位，禁拉伸。
   - **文字适配前置**（见下节）。
   - **层序**：组件内按「容器→图标→文本」自然顺序创建；全局原则「保原生内部序，只提图标和文本到顶」。形状存在 ≠ 渲染可见——图标消失先查物理 shape-tree 序（pic 节点须在卡片 sp 之后），再查 alpha，最后才重生资产。
   - 效果卫生：逐形状显式清 shadow/glow/softEdge/reflection；存后扫全部 XML（含 theme1.xml）确认 `outerShdw|glow|softEdge|reflection` 计数为零——theme 级阴影会漏过 slide 检查。
   - 线条克制：分隔线/边框须对应参考图可见线条，不因构图需要而加；渲染后偏深则减宽度/调色。
5. **渲染比对**：soffice→pdftoppm 转图，与参考图整页比对；拥挤区（图标槽、密卡、表格、底栏、回环箭头+标签）做 1:1 局部裁剪 QA。箭头与其标签视为一个视觉单元比对（头向/路径侧/粗细/标签位置）。
6. **多页组装**：每页独立重建（禁复制页 1 改页 2），按序合入同一 pptx；逐页资产/清单/预览按页号可溯源。

## 文字适配（text-fit preflight）

**先算后写，写必有证。** 每个产生 PPT 文本的代码路径（addText、run 拼接、表格单元、徽章）都要有 fit 证据：

```bash
python scripts/ppt_text_fit.py --text="升级方向不是少做事，而是更会定义、拆解、验收和复盘。" \
  --box 980x42 --font "Noto Sans CJK SC" --max-pt 22 --min-pt 12 --max-lines 1
```

- box 用导出像素坐标（`--slide-px/--slide-in` 换算 px_per_pt，如 1672px/13.33in ≈ 1.742）。
- 高危长文本加 `--target-pt <参考字号>`：输出 `required_box_px` 与 `box_deficit_px`，明示该修文本框还是缩字号。**缩字号是最后手段**——先扩框/去重复内边距/调列宽，文字明显小于同角色邻居时是布局缺陷。
- 行数锁：参考图一行的标签必须一行放完，两行标题保持两行；混排中英文标签（如 `看 diff、看运行结果`）比纯中文宽，预留余量。
- 紧凑 KPI 行（数值+单位+趋势箭头）：先切显式槽位（标签/数值/箭头槽），文本只在剩余区 fit，箭头锚在自己槽内；厚箭头用原生填充形非文本字形。
- 负号/加号/箭头/括号开头的文本：用 `--text=<value>` 等号传参，防 argparse 误读。
- 例外纪律：装饰性定字号小标签可手工字号，但须记入 `text_fit_report.json` 的 `exceptions`（bbox+理由），交付前经局部裁剪验证。报告保持紧凑：`called`/`notfits`/`exceptions`/代表高危长文本。

## 渲染 QA 依赖

- 整页比对需 LibreOffice（`soffice`）。本机未装时：改用 XML 结构校验降级（解包 pptx 后 grep：`a:ea typeface` 计数=中文 run 数、`outerShdw|glow|softEdge` 计数=0、末建文本 sp 位于 shape-tree 尾部=层序正确、`p:bg` 存在=原生背景），并在交付时明标 **draft（渲染 QA 未完成）**，不得宣称完成。
- 脚本 `imagetopptx_smoketest.py` 演示完整构建路径（背景填充/圆角调整/填充箭头/CJK 字体/效果清理/层序），soffice 在则自动转 PNG。

## 中文字体要点

- 度量与渲染：本机用 Noto Sans CJK SC 度量（ppt_text_fit.py 已把雅黑/黑体映射到 Noto，Windows 环境自动回落 C:/Windows/Fonts）。
- 产出字体名与度量字体名可不同：`run.font.name` 按目标打开环境写（如 Microsoft YaHei），本机渲染由 LibreOffice 替身近似，故版式漂移风险偏高，交付前渲染比对不可省。
- python-pptx 设完 `run.font.name` 后必须再设 OOXML `a:latin`/`a:ea`/`a:cs` typeface，否则 PowerPoint 回退宋体致版式漂移。
- 渲染图出现衬线/宋体字形 = 字体赋值失败，重查 run XML。

- **SVG 直绘示例**（对勾圆标，验证过的最小模板）：

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="44" fill="#1E2761"/>
  <path d="M30 52 L45 66 L72 36" stroke="#FFFFFF" stroke-width="9" fill="none"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

## 交付前验证

```bash
python scripts/check_rebuild_assets.py --asset-dir <资产目录>   # alpha/边距/边缘完整
```

- 交付物：最终 pptx 路径 + 渲染预览 + 资产目录 + 资产清单（每 image_asset 记 prompt/来源/切分操作）+ compact `text_fit_report.json`。
- 执行报告 `rebuild_execution_report.json` 末尾一次写就（compact）：input_prepared / visual_inventory_done / asset_classification_done / image_assets_done / text_fit_done / pptx_built / render_qa_done / local_crop_qa_done / validation_done。任一阶段做不了 → 停下报阻塞，禁静默跳过；用户催快 → 仍出最小证据并标注 draft。
- 不许仅凭「代码写完了」宣称完成——必须渲染亲验 + 至少一轮修验循环。
