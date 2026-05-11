#!/usr/bin/env python3
"""
AI 读书 —— 图书文本提取工具
支持 EPUB / Markdown / 纯文本 三种格式，输出结构化章节 JSON。
纯 Python 标准库实现，零外部依赖。
"""

import argparse
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

# ============================================================
# EPUB 解析
# ============================================================

NSMAP = {
    'n': 'urn:oasis:names:tc:opendocument:xmlns:package',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'opf': 'http://www.idpf.org/2007/opf',
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'ncx': 'http://www.daisy.org/z3986/2005/ncx/',
}


def _ns(tag, ns='n'):
    return f'{{{NSMAP[ns]}}}{tag}'


def _find_opf_path(zf):
    """从 META-INF/container.xml 中找 opf 文件路径"""
    container = zf.read('META-INF/container.xml')
    root = ET.fromstring(container)
    # root 命名空间是 urn:oasis:names:tc:opendocument:xmlns:container
    ns = 'urn:oasis:names:tc:opendocument:xmlns:container'
    for rf in root.iter(f'{{{ns}}}rootfile'):
        path = rf.get('full-path')
        if path:
            return path
    return None


def _parse_opf(zf, opf_path):
    """解析 opf，返回 metadata 和 spine"""
    opf_dir = os.path.dirname(opf_path)
    opf_data = zf.read(opf_path)
    root = ET.fromstring(opf_data)

    # metadata
    title = 'Untitled'
    creator = 'Unknown'
    for md_el in root.iter(_ns('metadata', 'n')):
        for t in md_el.iter(_ns('title', 'dc')):
            if t.text:
                title = t.text.strip()
        for c in md_el.iter(_ns('creator', 'dc')):
            if c.text:
                creator = c.text.strip()

    # spine — reading order
    spine = root.find(_ns('spine'))
    idrefs = []
    if spine is not None:
        for itemref in spine.iter(_ns('itemref')):
            ref = itemref.get('idref')
            if ref:
                idrefs.append(ref)

    # manifest — id → href 映射
    manifest = root.find(_ns('manifest'))
    id_to_href = {}
    if manifest is not None:
        for item in manifest.iter(_ns('item')):
            iid = item.get('id')
            href = item.get('href')
            if iid and href:
                id_to_href[iid] = href

    # 按 spine 顺序解析每个文件
    chapters = []
    for ref in idrefs:
        href = id_to_href.get(ref)
        if not href:
            continue
        # 相对 opf 目录解析
        full_path = os.path.normpath(os.path.join(opf_dir, href))
        try:
            raw = zf.read(full_path)
            text = _extract_xhtml_text(raw)
            if text.strip():
                # 用文件名当 fallback 标题
                fname = os.path.splitext(os.path.basename(href))[0]
                chapters.append({
                    'id': ref,
                    'source': full_path,
                    'title': fname,
                    'text': text.strip(),
                })
        except KeyError:
            continue

    # 尝试从 nav.xhtml 或 toc.ncx 获取更好的标题
    # 先查 toc.ncx
    for item in (manifest.iter(_ns('item')) if manifest is not None else []):
        iid = item.get('id')
        href = item.get('href')
        media_type = item.get('media-type', '')
        if not href:
            continue
        if 'toc' in (iid or '').lower() or media_type == 'application/x-dtbncx+xml':
            full_path = os.path.normpath(os.path.join(opf_dir, href))
            try:
                ncx_data = zf.read(full_path)
                _apply_ncx_titles(ncx_data, chapters)
            except (KeyError, ET.ParseError):
                pass
            break

    # 再查 nav.xhtml
    for item in (manifest.iter(_ns('item')) if manifest is not None else []):
        iid = item.get('id')
        href = item.get('href')
        media_type = item.get('media-type', '')
        if not href:
            continue
        if 'nav' in (iid or '').lower() or 'ncx' in (iid or '').lower():
            continue  # 已经处理过 ncx
        if media_type == 'application/xhtml+xml' and 'nav' in href.lower():
            full_path = os.path.normpath(os.path.join(opf_dir, href))
            try:
                nav_data = zf.read(full_path)
                _apply_nav_titles(nav_data, chapters)
            except (KeyError, ET.ParseError):
                pass
            break

    return title, creator, chapters


def _extract_xhtml_text(raw):
    """从 XHTML 中提取纯文本"""
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        # 清理后再试
        cleaned = re.sub(b'[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]', b'', raw)
        try:
            root = ET.fromstring(cleaned)
        except ET.ParseError:
            return ''
    return _iter_text(root)


def _iter_text(el):
    """递归提取元素中的文本"""
    parts = []
    # 跳过 style/script
    tag = el.tag.split('}')[-1] if '}' in el.tag else el.tag
    if tag.lower() in ('style', 'script', 'nav'):
        return ''
    if el.text:
        parts.append(el.text)
    for child in el:
        parts.append(_iter_text(child))
    if el.tail:
        parts.append(el.tail)
    result = ''.join(parts)
    # 清理多余空白
    result = re.sub(r'\s+', ' ', result)
    result = re.sub(r'\n\s*\n', '\n\n', result)
    return result


def _apply_ncx_titles(ncx_data, chapters):
    """用 toc.ncx 中的标题更新 chapters"""
    root = ET.fromstring(ncx_data)
    nav_map = root.find(_ns('navMap', 'ncx'))
    if nav_map is None:
        return
    # 构建 src → title 映射
    src_title = {}
    for np in nav_map.iter(_ns('navPoint', 'ncx')):
        content = np.find(_ns('content', 'ncx'))
        label = np.find(_ns('navLabel', 'ncx'))
        if content is None or label is None:
            continue
        src = content.get('src', '')
        text_el = label.find(_ns('text', 'ncx'))
        title = text_el.text.strip() if text_el is not None and text_el.text else ''
        if src and title:
            src_title[os.path.normpath(src)] = title

    for ch in chapters:
        # 匹配 source 中是否包含 ncx 引用的文件名
        ch_src = ch.get('source', '')
        for ncx_src, ncx_title in src_title.items():
            if ch_src.endswith(ncx_src) or ncx_src.endswith(ch_src.split('/')[-1]):
                ch['title'] = ncx_title
                break


def _apply_nav_titles(nav_data, chapters):
    """用 nav.xhtml 中的标题更新 chapters"""
    root = ET.fromstring(nav_data)
    # 找 nav 元素
    for nav in root.iter(f'{{{NSMAP["xhtml"]}}}nav'):
        ol = nav.find(f'{{{NSMAP["xhtml"]}}}ol')
        if ol is None:
            continue
        _extract_nav_links(ol, chapters)


def _extract_nav_links(ol, chapters, depth=0):
    """递归提取 nav 中的链接"""
    for li in ol.iter(f'{{{NSMAP["xhtml"]}}}li'):
        a = li.find(f'{{{NSMAP["xhtml"]}}}a')
        if a is not None:
            href = a.get('href', '')
            title = a.text.strip() if a.text else ''
            if href and title:
                # 只取 # 前的路径
                href = href.split('#')[0]
                for ch in chapters:
                    ch_src = ch.get('source', '')
                    if ch_src.endswith(href) or href.endswith(ch_src.split('/')[-1]):
                        if depth <= 1:  # 只取顶层章节标题
                            ch['title'] = title
                        break
        inner_ol = li.find(f'{{{NSMAP["xhtml"]}}}ol')
        if inner_ol is not None:
            _extract_nav_links(inner_ol, chapters, depth + 1)


def parse_epub(path):
    """解析 EPUB 文件，返回 (title, author, [chapter_dict])"""
    with zipfile.ZipFile(path, 'r') as zf:
        opf_path = _find_opf_path(zf)
        if not opf_path:
            raise ValueError('EPUB 中未找到 opf 文件')
        return _parse_opf(zf, opf_path)


# ============================================================
# PDF 解析（依赖 pdftotext）
# ============================================================

def _detect_chapter_boundaries(text):
    """
    智能检测章节边界，支持「第X章」「Chapter X」等格式。
    会排除目录（TOC）中带页码标记的条目和页眉重复项。
    """
    boundaries = []

    # 模式1：中文「第X章」——匹配单独一行的「第1章」或其变体
    # 匹配格式如：
    #                       第1章                   ← 章号独占一行
    #
    #          用排除法更快锁定答案                  ← 标题在下一行
    # 或：
    # 第 1 章   用排除法更快锁定答案 _003           ← TOC 条目（需跳过）
    for m in re.finditer(
        r'^\s*第\s*([一二三四五六七八九十百零\d]+)\s*章\s*$',
        text, re.MULTILINE
    ):
        chap_num = m.group(1).strip()
        pos = m.end()

        # 查找紧随其后的非空行作为章节标题
        rest = text[pos:pos+500]
        title_line = ''
        for line in rest.split('\n'):
            line = line.strip()
            if line and not line.startswith('') and len(line) > 2:
                # 检查是否像页码 + 书名页眉（如 "004 耶鲁学长给青少年的..."）
                if re.match(r'^\d{1,4}\s+耶鲁', line):
                    continue
                title_line = line
                break

        # 跳过 TOC 和页眉：标题以页码结尾（如 "快速淘汰无效选择 _063" 或 "锁定答案   005"）
        if re.search(r'[_\s]\d{3,4}\s*$', title_line):
            continue

        display_title = f'第{chap_num}章 {title_line}' if title_line else f'第{chap_num}章'
        boundaries.append((m.start(), pos, display_title))

    # 模式2：英文 "Chapter X"
    for m in re.finditer(
        r'^\s*Chapter\s+(\d+|[IVXLCDM]+)\s*[:\-–]\s*(.+)$',
        text, re.MULTILINE | re.IGNORECASE
    ):
        boundaries.append((
            m.start(), m.end(),
            f'Chapter {m.group(1)}: {m.group(2).strip()}'
        ))

    # 按位置排序
    boundaries.sort(key=lambda x: x[0])

    # 去重：合并距离过近的章节（< 500 字符以内，保留第一个，丢弃后续重复）
    deduped = []
    seen_titles = set()
    for b in boundaries:
        title_key = b[2][:20]  # 取标题前20字作为去重键
        if title_key in seen_titles:
            continue
        if deduped and (b[0] - deduped[-1][0]) < 500:
            continue
        seen_titles.add(title_key)
        deduped.append(b)
    boundaries = deduped

    return boundaries


def _clean_pdf_text(text):
    """清理 PDF 提取文本中的排版垃圾"""
    # 移除分页符
    text = text.replace('\f', '\n')
    # 移除页眉行（如 "004 耶鲁学长给青少年的算法启蒙书 THE COMPUTER ALWAYS WINS"）
    text = re.sub(
        r'^\s*\d{1,4}\s+耶鲁学长给青少年的算法启蒙书.*$',
        '', text, flags=re.MULTILINE
    )
    # 移除页眉反向：书名在前、页码在后
    text = re.sub(
        r'^耶鲁学长给青少年的算法启蒙书.*\d{1,4}\s*$',
        '', text, flags=re.MULTILINE
    )
    # 移除页码行（单独一行只有数字 1-4 位）
    text = re.sub(r'^\s*\d{1,4}\s*$', '', text, flags=re.MULTILINE)
    # 移除 ROMAN 页码
    text = re.sub(r'^\s*[IVXLCDM]+\s*$', '', text, flags=re.MULTILINE)
    # 移除 TOC 中的副标题行（如 "第 1 章   用排除法更快锁定答案 _003"）
    text = re.sub(
        r'^第\s+\d+\s+章\s+.+?_\d{3,4}\s*$',
        '', text, flags=re.MULTILINE
    )
    # 移除目录结构中的部分标记行
    text = re.sub(r'^第[一二三四五六七八九十]+\s+部分.*$', '', text, flags=re.MULTILINE)
    # 移除 "扫码获取""扫码加入书架" 等推广行
    text = re.sub(r'^扫码.*$', '', text, flags=re.MULTILINE)
    # 压缩多余空行
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()


def _guess_metadata_from_front(text):
    """从 PDF 文首猜测书名和作者（取连续长句作为书名）"""
    title = 'Untitled'
    author = 'Unknown'
    head = text[:5000]
    lines = [l.strip() for l in head.split('\n') if l.strip()]

    # 找书名：连续的无标点行，合并为完整书名
    title_lines = []
    for line in lines[:15]:
        if len(line) < 2 or len(line) > 80:
            if title_lines:
                break
            continue
        if any(kw in line for kw in ['www', '.com', 'http', '扫', 'ISBN', '定价',
                                      '著', '译', '编', '出版社', 'THE']):
            if not title_lines:
                continue
            else:
                break
        # 排除行首有特殊标记的行
        if line.startswith('●') or line.startswith('①') or line.startswith('（'):
            if not title_lines:
                continue
            else:
                break
        title_lines.append(line)
        if len(''.join(title_lines)) > 30:
            break

    if title_lines:
        title = ''.join(title_lines)
    else:
        # fallback: 取第一行有意义的文字
        for line in lines[:5]:
            if len(line) > 4 and not any(kw in line for kw in ['www', '扫', 'THE']):
                title = line
                break

    # 尝试匹配「[美] 作者名 著」或「作者名 著/编/译」模式
    author_patterns = [
        re.search(r'[\[（(【][^\]）)】]*?([\u4e00-\u9fa5]{2,4})[\]）)】】]\s*(著|编|译)', head),
        re.search(r'([\u4e00-\u9fa5]{2,4})\s*[·•‧]\s*[\u4e00-\u9fa5]{2,4}\s*(著|编|译)', head),
        re.search(r'(?:作者|Author)[：:]\s*(.+?)[\n\r]', head, re.IGNORECASE),
    ]
    for m in author_patterns:
        if m:
            author = m.group(1).strip()
            break

    return title, author


def parse_pdf(path):
    """解析 PDF 文件，使用 pdftotext 提取文本，按章节拆分"""
    import subprocess
    import tempfile

    # 检查 pdftotext 是否可用
    try:
        subprocess.run(['pdftotext', '-v'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        import platform
        sys = platform.system()
        if sys == 'Linux':
            install_cmd = 'sudo apt install poppler-utils    # Debian/Ubuntu\n      sudo yum install poppler-utils        # CentOS/RHEL'
        elif sys == 'Darwin':
            install_cmd = 'brew install poppler'
        elif sys == 'Windows':
            install_cmd = '下载 https://github.com/oschwartz10612/poppler-windows/releases/ 并加入 PATH'
        else:
            install_cmd = '请安装 poppler-utils（pdftotext）'
        raise RuntimeError(
            f'[错误] 需要 pdftotext 来解析 PDF，但未找到。\n'
            f'       请安装 poppler-utils：\n'
            f'       {install_cmd}'
        )

    # 用 pdftotext 提取文本
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w+') as tmp:
        output_path = tmp.name

    try:
        subprocess.run(
            ['pdftotext', '-layout', path, output_path],
            capture_output=True, check=True, timeout=120
        )
        with open(output_path, 'r', encoding='utf-8', errors='replace') as f:
            raw_text = f.read()
    finally:
        if os.path.exists(output_path):
            os.unlink(output_path)

    # 清理文本
    text = _clean_pdf_text(raw_text)

    # 检测章节边界
    boundaries = _detect_chapter_boundaries(text)

    # 提取元数据
    title, author = _guess_metadata_from_front(text)

    chapters = []
    if not boundaries:
        # 没有检测到章节标记，整本书当一章
        chapters.append({
            'id': 'ch_1',
            'source': path,
            'title': '全文',
            'text': text,
        })
    else:
        # 前言/序言：第一个章节之前的内容
        front_text = text[:boundaries[0][0]].strip()
        if front_text:
            chapters.append({
                'id': 'front_matter',
                'source': path,
                'title': '前言与导读',
                'text': front_text,
            })

        # 逐章分割
        for i, (start, end, chap_title) in enumerate(boundaries):
            chap_end = boundaries[i + 1][0] if i + 1 < len(boundaries) else len(text)
            body = text[start:chap_end].strip()
            # 清理章节标题行自身
            body_lines = body.split('\n', 1)
            body = body_lines[1].strip() if len(body_lines) > 1 else ''
            chapters.append({
                'id': f'ch_{i + 1}',
                'source': path,
                'title': chap_title,
                'text': body,
            })

        # 附录/后记：检测最后一个章节之后是否有真正的附录内容
        if boundaries:
            last_ch = chapters[-1]
            # 真正的后记/附录通常以关键词开头，且与正文不重叠
            tail_text = text[boundaries[-1][1]:].strip()
            # 只有尾部长于 200 字 且 包含附录关键词时才添加
            if len(tail_text) > 200 and re.search(
                r'^(后\s*记|附\s*录|延伸阅读|附录|Postscript|Appendix)',
                tail_text, re.MULTILINE | re.IGNORECASE
            ):
                # 确保 tail 和最后一章正文不重叠
                if tail_text not in last_ch['text']:
                    chapters.append({
                        'id': 'appendix',
                        'source': path,
                        'title': '附录与后记',
                        'text': tail_text,
                    })

    return title, author, chapters


# ============================================================
# Markdown / 纯文本 解析
# ============================================================

def parse_markdown(path):
    """解析 Markdown 文件，按标题分章"""
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    return _split_by_headings(text)


def parse_text(path):
    """解析纯文本文件，按空行或固定字数分节"""
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    # 按两个以上换行分节
    sections = re.split(r'\n{3,}', text)
    chapters = []
    for i, sec in enumerate(sections, 1):
        sec = sec.strip()
        if not sec:
            continue
        # 取第一行当标题
        lines = sec.split('\n')
        title = lines[0].strip()[:60] if lines[0].strip() else f'第{i}节'
        chapters.append({
            'id': f'sec_{i}',
            'source': path,
            'title': title,
            'text': sec,
        })
    return 'Untitled', 'Unknown', chapters


def _split_by_headings(text):
    """按 Markdown 标题分章"""
    # 匹配 # 开头的标题
    pattern = re.compile(r'^(#{1,4})\s+(.+)$', re.MULTILINE)
    matches = list(pattern.finditer(text))

    chapters = []
    if not matches:
        # 无标题，整本当一章
        chapters.append({
            'id': 'ch_1',
            'source': '',
            'title': '全文',
            'text': text.strip(),
        })
        return 'Untitled', 'Unknown', chapters

    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = m.group(2).strip()
        body = text[start:end].strip()
        # 去掉标题行本身
        body_lines = body.split('\n', 1)
        body = body_lines[1].strip() if len(body_lines) > 1 else ''
        chapters.append({
            'id': f'ch_{i + 1}',
            'source': '',
            'title': title,
            'text': body,
        })

    # 尝试从第一段获取书名和作者
    title = 'Untitled'
    author = 'Unknown'
    first_chunk = chapters[0]['text'][:500] if chapters else ''
    # 简单的 metadata 猜测
    meta_match = re.search(r'^title:\s*(.+)$', first_chunk, re.MULTILINE | re.IGNORECASE)
    if meta_match:
        title = meta_match.group(1).strip()
    author_match = re.search(r'^author:\s*(.+)$', first_chunk, re.MULTILINE | re.IGNORECASE)
    if author_match:
        author = author_match.group(1).strip()

    return title, author, chapters


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='提取图书文本，输出章节 JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            '示例:\n'
            '  python3 extract_book.py 图书.pdf --pretty\n'
            '  python3 extract_book.py 图书.epub -o output.json\n'
            '  python3 extract_book.py 图书.md --pretty\n'
        )
    )
    parser.add_argument('input', help='输入文件路径 (.epub / .md / .txt / .pdf)')
    parser.add_argument('-o', '--output', help='输出 JSON 文件路径（默认 stdout）')
    parser.add_argument('--pretty', action='store_true', help='美化 JSON 输出')
    args = parser.parse_args()

    path = args.input
    if not os.path.exists(path):
        print(f'[错误] 文件不存在: {path}', file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(path)[1].lower()
    filesize = os.path.getsize(path)
    print(f'[信息] 解析: {path} ({filesize / 1024:.0f} KB)', file=sys.stderr)

    try:
        if ext == '.epub':
            title, author, chapters = parse_epub(path)
        elif ext == '.md':
            title, author, chapters = parse_markdown(path)
        elif ext == '.txt':
            title, author, chapters = parse_text(path)
        elif ext == '.pdf':
            title, author, chapters = parse_pdf(path)
        else:
            # 按内容猜测
            with open(path, 'rb') as f:
                head = f.read(1024)
            if head.startswith(b'PK'):
                title, author, chapters = parse_epub(path)
            elif head.startswith(b'%PDF'):
                title, author, chapters = parse_pdf(path)
            else:
                try:
                    text = head.decode('utf-8')
                    if text.lstrip().startswith('#') or text.lstrip().startswith('-') or '[TOC]' in text:
                        title, author, chapters = parse_markdown(path)
                    else:
                        title, author, chapters = parse_text(path)
                except UnicodeDecodeError:
                    title, author, chapters = parse_text(path)

        result = {
            'title': title,
            'author': author,
            'source': os.path.abspath(path),
            'total_chapters': len(chapters),
            'total_chars': sum(len(ch['text']) for ch in chapters),
            'chapters': chapters,
        }

        indent = 2 if args.pretty else None
        output = json.dumps(result, ensure_ascii=False, indent=indent)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f'[完成] 已写入 {args.output}', file=sys.stderr)
        else:
            print(output)

        # 输出摘要信息到 stderr
        empty_chs = [ch['id'] for ch in chapters if len(ch['text']) < 50]
        print(
            f'[完成] 书名: {title} | 作者: {author} | '
            f'章节: {len(chapters)} | 总字数: {result["total_chars"]}',
            file=sys.stderr
        )
        if empty_chs:
            print(f'[警告] 以下章节内容过短: {", ".join(empty_chs)}', file=sys.stderr)

    except RuntimeError as e:
        print(f'{e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'[错误] 解析失败: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
