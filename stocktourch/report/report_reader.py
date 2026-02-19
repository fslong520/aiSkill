import os
import re
from PyPDF2 import PdfReader
import tempfile


def convert_pdf_to_txt(pdf_path: str):
    """
    将 PDF 文件转换为 TXT 文本文件
    
    Args:
        pdf_path: PDF 文件路径
    
    Returns:
        TXT 文件路径
    """
    # 创建临时 TXT 文件
    temp_fd, temp_path = tempfile.mkstemp(suffix='.txt')
    
    try:
        # 读取 PDF 内容
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"
        
        # 写入临时 TXT 文件
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as temp_file:
            temp_file.write(text_content)
        
        return temp_path
        
    except Exception as e:
        # 如果出错，关闭文件描述符
        os.close(temp_fd)
        raise e


def extract_financial_highlights(text_content: str) -> dict:
    """
    从财报文本中提取关键财务指标
    
    Args:
        text_content: 财报文本内容
    
    Returns:
        包含关键指标的字典
    """
    highlights = {}
    
    # 尝试提取常见财务指标（使用正则表达式）
    # 营业收入
    revenue_match = re.search(r'营业总收入 [\s:：]*(\d+[.,]\d+)\s*(亿元 | 万元)?', text_content[:5000])
    if revenue_match:
        value = revenue_match.group(1).replace(',', '')
        unit = revenue_match.group(2) if revenue_match.group(2) else '亿元'
        highlights['营业收入'] = f"{value}{unit}"
    
    # 归母净利润
    profit_match = re.search(r'归属于上市公司股东的净利润 [\s:：]*(\d+[.,]\d+)\s*(亿元 | 万元)?', text_content[:5000])
    if profit_match:
        value = profit_match.group(1).replace(',', '')
        unit = profit_match.group(2) if profit_match.group(2) else '亿元'
        highlights['归母净利润'] = f"{value}{unit}"
    
    # 扣非净利润
    deducted_profit_match = re.search(r'扣除非经常性损益后的净利润 [\s:：]*(\d+[.,]\d+)\s*(亿元 | 万元)?', text_content[:5000])
    if deducted_profit_match:
        value = deducted_profit_match.group(1).replace(',', '')
        unit = deducted_profit_match.group(2) if deducted_profit_match.group(2) else '亿元'
        highlights['扣非净利润'] = f"{value}{unit}"
    
    # 每股收益
    eps_match = re.search(r'基本每股收益 [\s:：]*(\d+[.,]\d+)\s*元', text_content[:5000])
    if eps_match:
        value = eps_match.group(1).replace(',', '')
        highlights['基本每股收益'] = f"{value}元"
    
    # 净资产收益率
    roe_match = re.search(r'加权平均净资产收益率 [\s:：]*([+-]?\d+[.,]\d+)\s*%', text_content[:5000])
    if roe_match:
        value = roe_match.group(1).replace(',', '')
        highlights['ROE'] = f"{value}%"
    
    # 总资产
    assets_match = re.search(r'总资产 [\s:：]*(\d+[.,]\d+)\s*(亿元 | 万元)?', text_content[:5000])
    if assets_match:
        value = assets_match.group(1).replace(',', '')
        unit = assets_match.group(2) if assets_match.group(2) else '亿元'
        highlights['总资产'] = f"{value}{unit}"
    
    # 总负债
    liabilities_match = re.search(r'总负债 [\s:：]*(\d+[.,]\d+)\s*(亿元 | 万元)?', text_content[:5000])
    if liabilities_match:
        value = liabilities_match.group(1).replace(',', '')
        unit = liabilities_match.group(2) if liabilities_match.group(2) else '亿元'
        highlights['总负债'] = f"{value}{unit}"
    
    # 经营活动现金流净额
    cash_flow_match = re.search(r'经营活动产生的现金流量净额 [\s:：]*(\d+[.,]\d+)\s*(亿元 | 万元)?', text_content[:5000])
    if cash_flow_match:
        value = cash_flow_match.group(1).replace(',', '')
        unit = cash_flow_match.group(2) if cash_flow_match.group(2) else '亿元'
        highlights['经营现金流净额'] = f"{value}{unit}"
    
    return highlights


def get_report_summary(pdf_path: str, stock_name: str) -> dict:
    """
    获取财报摘要信息
    
    Args:
        pdf_path: PDF 财报文件路径
        stock_name: 股票名称
    
    Returns:
        包含财报摘要的字典
    """
    try:
        # 转换 PDF 为 TXT
        txt_path = convert_pdf_to_txt(pdf_path)
        
        # 读取 TXT 内容
        with open(txt_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        # 提取文件名中的年份信息
        filename = os.path.basename(pdf_path)
        year_match = re.search(r'(\d{4}) 年', filename)
        if year_match:
            year = year_match.group(1)
        else:
            # 尝试从内容中查找年份
            year_match = re.search(r'(\d{4}) 年度报告', text_content[:2000])
            year = year_match.group(1) if year_match else '未知'
        
        # 提取关键指标
        highlights = extract_financial_highlights(text_content)
        
        # 生成摘要
        summary = {
            'year': year,
            'stock_name': stock_name,
            'highlights': highlights,
            'text_preview': text_content[:3000],  # 前 3000 字符作为预览
            'total_length': len(text_content),
            'txt_file': txt_path
        }
        
        return summary
        
    except Exception as e:
        print(f"处理财报失败：{e}")
        return {
            'year': '未知',
            'stock_name': stock_name,
            'highlights': {},
            'text_preview': '',
            'error': str(e)
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法：python report_reader.py <pdf 文件路径>")
        print("示例：python report_reader.py /path/to/600096_云天化_云天化 2025 年第三季度报告_1224753834.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(pdf_path):
        print(f"❌ 文件不存在：{pdf_path}")
        sys.exit(1)
    
    try:
        txt_path = convert_pdf_to_txt(pdf_path)
        print(f"✅ PDF 文件已转换为 TXT 文件：{txt_path}")
        
        # 读取并显示部分内容
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"\n📄 文件大小：{len(content)} 字符")
            print(f"\n📋 内容预览（前 500 字符）:\n{content[:500]}...")
    except Exception as e:
        print(f"❌ 转换失败：{e}")
        sys.exit(1)
