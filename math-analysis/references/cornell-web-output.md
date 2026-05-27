# Cornell Web Output Reference

## Page sections

Use these section labels unless the user asks for another style:

- `题目`
- `这一题考什么`
- `要记住的知识`
- `错因分析`
- `正确解法`
- `易错提醒`
- `考试怎么做最快`
- `同类题识别`
- `练 3 道`
- `最后记一句`

## Cornell layout

The page should feel like a useful student note, not a marketing page.

- Left column: short cue cards only. Keep each cue under 3 lines.
- Main column: full explanation and algebra steps.
- Top tools: theme buttons only.
- Floating pen tools: appear beside selected text and include highlighter colors, comment, and a rightmost targeted undo button.
- Bottom summary: short, direct, and memorable.

## Visual modeling

Some math wrong questions need a picture before the student can really see the mistake. When a visual model helps, add it inside the solution steps.

Use diagrams for:

- 集合、不等式、取值范围: number lines, interval bars, open/closed endpoints, discrete integer or natural-number points.
- 函数和二次函数符号: coordinate axes, function curves, roots, positive/negative regions, key points, monotonic intervals.
- 几何题: triangles, circles, auxiliary lines, equal-angle/equal-length marks, parallel marks, area/length relations.
- 解析几何和动点题: coordinate sketches, locus hints, moving point positions, boundary cases.
- 面积、概率、排列组合: area models, grids, tree-like arrangements, counted regions.

Diagram rules:

- Put the diagram right after the step it explains, not in a separate gallery.
- Add a one-sentence caption starting with `图形看法：` or another student-friendly cue.
- Prefer inline SVG so the page stays standalone. Use the shared `.diagram`, `.axis`, `.curve`, `.focus`, `.dot`, `.dot-on`, `.guide`, `.soft-fill`, and `.tick` classes when possible.
- Coordinate SVGs must be numerically honest: axes, roots, intercepts, vertices, endpoints, and labeled points should use one consistent coordinate mapping. If the graph says the root is `(4,0)`, the curve must cross the x-axis exactly at the visual tick labeled `4`.
- Show endpoints honestly: open circles for excluded endpoints, filled dots for included points, and separate dots for `x∈N` or `x∈Z`.
- Keep the visual tied to the exam method. Do not add decorative illustrations, complex 3D, or advanced constructions that are not needed.

## Morandi palettes

Use restrained, low-saturation colors.

- Yellow: background `#f5f0df`, surface `#fffaf0`, accent `#bca66a`, ink `#3f3a2f`.
- Green: background `#e8eee5`, surface `#f7faf4`, accent `#7f9a83`, ink `#303a32`.
- Blue: background `#e7edf1`, surface `#f7fafb`, accent `#7f9bab`, ink `#2d3840`.
- Purple: background `#eee8f1`, surface `#fbf8fc`, accent `#9a88a5`, ink `#3c3440`.

Keep body text dark and contrast high. Avoid saturated gradients and decorative blobs.

## Student note behavior

The page should feel like a student is marking a notebook, not drawing boxes on a screenshot.

Minimum controls:

- A floating pen toolbar that appears near selected text or clicked marks.
- Yellow, green, and blue highlighter choices inside that floating toolbar.
- Add comment inside the floating toolbar.
- A rightmost targeted undo button inside the floating toolbar.
- A comment list showing each written comment.
- Highlighter and comment can be applied to the same text mark.

Minimum interaction:

1. The user selects text anywhere in the learning page content: title metadata, cue column, main notes, exercises, or final summary.
2. The floating pen toolbar appears next to the selection. The user should not need to move to a fixed right-side toolbar.
3. Clicking a highlighter wraps the selected text with a visible highlight span.
4. If the selected or clicked text is already highlighted, clicking add comment should attach the comment to that same mark while preserving the highlight.
5. If the selected or clicked text is already a comment mark, clicking a highlighter should add or change its highlight color while preserving the comment.
6. Clicking add comment on plain selected text asks for a short note and wraps the selected text with a comment mark.
7. The comment appears in a margin/list area.
8. Clicking a comment scrolls back to the marked text.
9. Save note changes in localStorage when possible.
10. Targeted undo should remove the currently clicked mark or the mark containing the current selection. If no target mark is active, the undo button may stay disabled or show a short prompt.
11. The floating toolbar should disappear when the user clicks normal content, clicks blank space, presses Escape, or scrolls without an active text selection. It should not remain parked on the page after a note action is finished.

Implementation note: the selectable study surface should cover all learning content, not only the problem or main note column. Keep tool buttons outside the saved/annotatable surface so repeated saves do not break button event handlers.

The top keyword/tag chips should not contain the final answer. Put the answer inside the solution section or final answer block instead.

Do not use drag-to-draw rectangles or older rectangle-marking controls.

If the source includes a problem photo, place the image inside the problem area and use `max-width: 100%`. The highlighter/comment tools may work on surrounding explanatory text; if image annotation is needed, use a caption or nearby text comment rather than a box. If the source is text only, render the problem text as selectable text.

## Math writing

For weak students, avoid jumping from one equation to the final result.

Good:

```text
8c - 200 = -224
8c = -24
c = -3
```

Bad:

```text
代入得 c = -3
```

When the student's error is conceptual, name the exact false assumption:

`错解不能代入被看错的那条方程。`

## File naming

Prefer:

`/Users/marsfish/AI/report/YYYY-MM-DD_数学分析_<短题名>.html`

If the title contains unsafe filename characters, replace them with `_`.
