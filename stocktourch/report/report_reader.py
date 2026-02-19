#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财报内容提取器
从PDF财报中提取文本内容，供AI分析
"""

import os
import re


def extract_text_from_pdf(pdf_path: str, max_pages: int = 50) -> str:
    """
    从PDF文件中提取文本内容
    
    Args:
        pdf_path: PDF文件路径
        max_pages: 最大提取页数（财报通常很长，限制提取页数以避免超限）
    
    Returns:
        提取的文本内容
    """
    text_content = []
    
    # 尝试使用pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            pages_to_extract = min(total_pages, max_pages)
            
            for i, page in enumerate(pdf.pages[:pages_to_extract]):
                page_text = page.extract_text()
                if page_text:
                    text_content.append(f"--- 第{i+1}页 ---")
                    text_content.append(page_text)
            
            if total_pages > max_pages:
                text_content.append(f"\n... (共{total_pages}页，仅提取前{max_pages}页)")
                
        return "\n\n".join(text_content)
    except ImportError:
        pass
    
    # 备用方案：尝试PyPDF2
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        pages_to_extract = min(total_pages, max_pages)
        
        for i in range(pages_to_extract):
            page = reader.pages[i]
            page_text = page.extract_text()
            if page_text:
                text_content.append(f"--- 第{i+1}页 ---")
                text_content.append(page_text)
        
        if total_pages > max_pages:
            text_content.append(f"\n... (共{total_pages}页，仅提取前{max_pages}页)")
            
        return "\n\n".join(text_content)
    except Exception as e:
        return f"PDF提取失败: {str(e)}"


def extract_financial_highlights(text: str) -> dict:
    """
    从财报文本中提取关键财务指标
    
    Args:
        text: 财报文本内容
    
    Returns:
        包含关键指标的字典
    """
    highlights = {}
    
    # 提取营业收入
    patterns = {
        "营业收入": r"营业收入[^\d]*([\d,]+(?:\.\d+)?)\s*(?:亿元|万元|万|亿)",
        "净利润": r"净利润[^\d]*([\d,]+(?:\.\d+)?)\s*(?:亿元|万元|万|亿)",
        "总资产": r"总资产[^\d]*([\d,]+(?:\.\d+)?)\s*(?:亿元|万元|万|亿)",
        "净资产": r"净资产[^\d]*([\d,]+(?:\.\d+)?)\s*(?:亿元|万元|万|亿)",
        "每股收益": r"每股收益[^\d]*([\d,]+(?:\.\d+)?)\s*元",
        "毛利率": r"毛利率[^\d]*([\d,]+(?:\.\d+)?)\s*%",
        "净利率": r"净利率[^\d]*([\d,]+(?:\.\d+)?)\s*%",
        "ROE": r"净资产收益率[^\d]*([\d,]+(?:\.\d+)?)\s*%",
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            highlights[key] = match.group(1)
    
    return highlights


def get_report_summary(pdf_path: str, stock_name: str = "") -> dict:
    """
    获取财报摘要信息
    
    Args:
        pdf_path: PDF文件路径
        stock_name: 股票名称
    
    Returns:
        包含摘要信息的字典
    """
    # 提取文本
    text = extract_text_from_pdf(pdf_path)
    
    # 提取关键指标
    highlights = extract_financial_highlights(text)
    
    # 尝试提取年报年份
    year_match = re.search(r"(\d{4})\s*年\s*(?:年度)?\s*报告", text)
    year = year_match.group(1) if year_match else "未知"
    
    return {
        "file": os.path.basename(pdf_path),
        "stock_name": stock_name,
        "year": year,
        "highlights": highlights,
        "text_preview": text[:5000] if text else "",  # 预览前5000字符
        "full_text": text,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python report_reader.py <pdf文件路径>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    result = get_report_summary(pdf_path)
    print(f"文件: {result['file']}")
    print(f"年份: {result['year']}")
    print(f"关键指标: {result['highlights']}")
    print(f"\n内容预览 (前2000字):\n{result['text_preview'][:2000]}")
