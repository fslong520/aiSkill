#!/bin/bash
# -*- coding: utf-8 -*-
"""
文件智能整理器主执行脚本
提供命令行接口和自然语言处理功能
"""

set -e  # 遇到错误立即退出

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON_SCRIPT="$SKILL_DIR/main.py"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    if [[ "$DEBUG" == "1" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $1"
    fi
}

# 显示帮助信息
show_help() {
    cat << EOF
文件智能整理器

用法: $0 <命令> [选项] <目录>

命令:
    organize         传统文件整理
    smart-organize   四阶段智能整理（推荐）
    analyze-only     仅执行文件分析
    enhanced-analyze 增强目录分析（含tree和多方案）
    plan-only        仅生成整理方案
    execute-plan     执行整理方案
    undo-session     撤销整理会话
    list-sessions    列出整理会话
    scan-duplicates  仅扫描重复文件
    generate-report  生成整理报告
    help            显示此帮助信息

选项:
    -c, --config FILE    指定配置文件路径
    -d, --dry-run        试运行模式（不实际移动文件）
    -v, --verbose        详细输出模式
    -f, --format FORMAT  报告格式 (markdown/json/html)
    --debug             调试模式

示例:
    $0 organize /home/user/Downloads
    $0 smart-organize /home/user/Downloads
    $0 analyze-only /home/user/Downloads
    $0 enhanced-analyze /home/user/Downloads
    $0 plan-only /home/user/Downloads
    $0 execute-plan /home/user/Downloads --plan plan.json
    $0 undo-session SESSION_ID
    $0 list-sessions
    $0 scan-duplicates /home/user/Pictures
    $0 generate-report /home/user/Downloads -f json

自然语言使用:
    $0 "帮我整理下载文件夹"
    $0 "分析并制定文件分类方案"
    $0 "按AI建议整理我的文档"
    $0 "检测并处理重复的照片"
EOF
}

# 检查Python环境
check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "未找到 Python 3，请先安装 Python 3"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    log_debug "Python 版本: $PYTHON_VERSION"
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖..."
    
    # 检查PyYAML
    if ! python3 -c "import yaml" 2>/dev/null; then
        log_warn "缺少 PyYAML 依赖，正在安装..."
        pip3 install PyYAML --user || {
            log_error "安装 PyYAML 失败，请手动安装: pip3 install PyYAML"
            exit 1
        }
    fi
    
    log_info "依赖检查完成"
}

# 解析自然语言命令
parse_natural_language() {
    local input="$1"
    local lower_input=$(echo "$input" | tr '[:upper:]' '[:lower:]')
    
    # 整理相关关键词
    if echo "$lower_input" | grep -E "(整理|分类|organize|sort)" >/dev/null; then
        COMMAND="organize"
        
        # 提取目录
        if echo "$lower_input" | grep -E "(下载|download)" >/dev/null; then
            TARGET_DIR="$HOME/Downloads"
        elif echo "$lower_input" | grep -E "(文档|document)" >/dev/null; then
            TARGET_DIR="$HOME/Documents"
        elif echo "$lower_input" | grep -E "(桌面|desktop)" >/dev/null; then
            TARGET_DIR="$HOME/Desktop"
        elif echo "$lower_input" | grep -E "(图片|照片|image|photo)" >/dev/null; then
            TARGET_DIR="$HOME/Pictures"
        else
            # 尝试从输入中提取目录名
            for dir in "$HOME"/{Downloads,Documents,Desktop,Pictures,Videos}; do
                dir_name=$(basename "$dir")
                if echo "$lower_input" | grep -E "$dir_name" >/dev/null; then
                    TARGET_DIR="$dir"
                    break
                fi
            done
        fi
        
        # 检查是否指定了试运行
        if echo "$lower_input" | grep -E "(试试|预览|dry|preview)" >/dev/null; then
            DRY_RUN="--dry-run"
        fi
        
    # 重复文件检测相关关键词
    elif echo "$lower_input" | grep -E "(重复|duplicate|清理|clean)" >/dev/null; then
        COMMAND="scan-duplicates"
        
        # 提取目录
        if echo "$lower_input" | grep -E "(照片|图片|photo|image)" >/dev/null; then
            TARGET_DIR="$HOME/Pictures"
        elif echo "$lower_input" | grep -E "(下载|download)" >/dev/null; then
            TARGET_DIR="$HOME/Downloads"
        else
            TARGET_DIR="$HOME"
        fi
    
    # 报告生成相关关键词
    elif echo "$lower_input" | grep -E "(报告|report|生成)" >/dev/null; then
        COMMAND="generate-report"
        TARGET_DIR="$HOME"
        
        # 检查报告格式
        if echo "$lower_input" | grep -E "(json|html)" >/dev/null; then
            REPORT_FORMAT=$(echo "$lower_input" | grep -oE "(json|html)")
        fi
    
    else
        log_error "无法理解的命令: $input"
        show_help
        exit 1
    fi
    
    log_info "解析自然语言命令: $COMMAND ${TARGET_DIR:-[未指定目录]}"
}

# 主函数
main() {
    # 初始化变量
    COMMAND=""
    TARGET_DIR=""
    CONFIG_FILE=""
    DRY_RUN=""
    VERBOSE=""
    REPORT_FORMAT="markdown"
    DEBUG=${DEBUG:-0}
    
    # 检查参数
    if [[ $# -eq 0 ]]; then
        show_help
        exit 1
    fi
    
    # 检查是否为自然语言输入
    if [[ $# -eq 1 ]] && [[ "$1" =~ [[:alpha:][:space:]] ]]; then
        parse_natural_language "$1"
        shift
    else
        # 解析命令行参数
        while [[ $# -gt 0 ]]; do
            case $1 in
                organize|smart-organize|analyze-only|enhanced-analyze|plan-only|scan-duplicates|generate-report)
                    COMMAND="$1"
                    shift
                    ;;
                execute-plan)
                    COMMAND="$1"
                    shift
                    PLAN_FILE=""
                    # 获取plan参数
                    while [[ $# -gt 0 ]]; do
                        case $1 in
                            --plan)
                                PLAN_FILE="$2"
                                shift 2
                                ;;
                            *)
                                if [[ -z "$TARGET_DIR" ]]; then
                                    TARGET_DIR="$1"
                                fi
                                shift
                                ;;
                        esac
                    done
                    ;;
                undo-session|list-sessions)
                    COMMAND="$1"
                    if [[ "$1" == "undo-session" ]]; then
                        SESSION_ID="$2"
                        shift 2
                    else
                        shift
                    fi
                    ;;
                -c|--config)
                    CONFIG_FILE="$2"
                    shift 2
                    ;;
                -d|--dry-run)
                    DRY_RUN="--dry-run"
                    shift
                    ;;
                -v|--verbose)
                    VERBOSE="--verbose"
                    shift
                    ;;
                -f|--format)
                    REPORT_FORMAT="$2"
                    shift 2
                    ;;
                --debug)
                    DEBUG=1
                    shift
                    ;;
                -h|--help)
                    show_help
                    exit 0
                    ;;
                *)
                    if [[ -z "$TARGET_DIR" ]]; then
                        TARGET_DIR="$1"
                    else
                        log_error "未知参数: $1"
                        show_help
                        exit 1
                    fi
                    shift
                    ;;
            esac
        done
    fi
    
    # 验证必需参数
    if [[ -z "$COMMAND" ]]; then
        log_error "必须指定命令"
        show_help
        exit 1
    fi
    
    if [[ -z "$TARGET_DIR" ]]; then
        log_error "必须指定目标目录"
        show_help
        exit 1
    fi
    
    # 检查目录是否存在
    if [[ ! -d "$TARGET_DIR" ]]; then
        log_error "目录不存在: $TARGET_DIR"
        exit 1
    fi
    
    # 检查环境
    check_python
    check_dependencies
    
    # 构建Python命令
    if [[ "$COMMAND" == "undo-session" ]]; then
        PYTHON_CMD="python3 $PYTHON_SCRIPT $COMMAND '$SESSION_ID'"
    elif [[ "$COMMAND" == "list-sessions" ]]; then
        PYTHON_CMD="python3 $PYTHON_SCRIPT $COMMAND"
        if [[ -n "$STATUS_FILTER" ]]; then
            PYTHON_CMD+=" --status $STATUS_FILTER"
        fi
    elif [[ "$COMMAND" == "execute-plan" ]]; then
        PYTHON_CMD="python3 $PYTHON_SCRIPT $COMMAND '$TARGET_DIR' --plan '$PLAN_FILE'"
    else
        PYTHON_CMD="python3 $PYTHON_SCRIPT $COMMAND '$TARGET_DIR'"
    fi
    
    if [[ -n "$CONFIG_FILE" ]] && [[ "$COMMAND" != "undo-session" ]] && [[ "$COMMAND" != "list-sessions" ]]; then
        PYTHON_CMD+=" --config '$CONFIG_FILE'"
    fi
    
    if [[ -n "$DRY_RUN" ]]; then
        PYTHON_CMD+=" --dry-run"
    fi
    
    if [[ -n "$VERBOSE" ]]; then
        PYTHON_CMD+=" --verbose"
    fi
    
    if [[ "$COMMAND" == "generate-report" ]]; then
        PYTHON_CMD+=" --format $REPORT_FORMAT"
    fi
    
    # 显示执行信息
    log_info "执行命令: $COMMAND"
    log_info "目标目录: $TARGET_DIR"
    [[ -n "$CONFIG_FILE" ]] && log_info "配置文件: $CONFIG_FILE"
    [[ -n "$DRY_RUN" ]] && log_info "模式: 试运行"
    [[ "$COMMAND" == "generate-report" ]] && log_info "报告格式: $REPORT_FORMAT"
    
    # 执行Python脚本
    log_info "开始执行..."
    eval $PYTHON_CMD
    
    local exit_code=$?
    
    if [[ $exit_code -eq 0 ]]; then
        log_info "执行完成"
    else
        log_error "执行失败，退出码: $exit_code"
        exit $exit_code
    fi
}

# 脚本入口点
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi