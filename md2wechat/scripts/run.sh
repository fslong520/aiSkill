#!/bin/bash
#
# md2wechat - Smart entry point with auto binary provisioning
# Philosophy: Simple, fast, fail gracefully
#

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

REPO="geekjourneyx/md2wechat-skill"
BINARY_NAME="md2wechat"

# Cache directories (following XDG conventions)
CACHE_HOME="${XDG_CACHE_HOME:-${HOME}/.cache}/claude"
BIN_DIR="${CACHE_HOME}/bin"
VERSION_FILE="${CACHE_HOME}/md2wechat-skill/version.json"

# GitHub release URL template
RELEASE_URL="https://github.com/${REPO}/releases/download"

# Minimum binary size (100KB - protects against empty/corrupted downloads)
MIN_BINARY_SIZE=102400

# Error codes
ERR_NO_DOWNLOAD_TOOL=2
ERR_DOWNLOAD_FAILED=3
ERR_UNSUPPORTED_PLATFORM=4
ERR_CACHE_DIR=5
ERR_BINARY_INVALID=6

# =============================================================================
# LOGGING UTILITIES - User-friendly output
# =============================================================================

# Check if we're in an interactive terminal with color support
use_color() {
    [[ -t 2 ]] && [[ "$TERM" != "dumb" ]]
}

# Print symbols with/without color
success() {
    if use_color; then
        echo "  $1" >&2
    else
        echo "  [OK] $1" >&2
    fi
}

info() {
    echo "  $1" >&2
}

error() {
    if use_color; then
        echo "" >&2
        echo "  $1" >&2
    else
        echo "" >&2
        echo "  [ERROR] $1" >&2
    fi
    shift
    for msg in "$@"; do
        echo "  $msg" >&2
    done
    echo "" >&2
}

# =============================================================================
# PLATFORM DETECTION
# =============================================================================

detect_platform() {
    local os arch

    os=$(uname -s | tr '[:upper:]' '[:lower:]')
    arch=$(uname -m)

    case "$arch" in
        x86_64|amd64) arch="amd64" ;;
        arm64|aarch64) arch="arm64" ;;
        i386|i686) arch="386" ;;
        *)
        error "Unsupported architecture: $arch"
        return $ERR_UNSUPPORTED_PLATFORM
        ;;
    esac

    case "$os" in
        darwin|linux|msys*|mingw*|cygwin*)
            [[ "$os" == msys* ]] || [[ "$os" == mingw* ]] || [[ "$os" == cygwin* ]] && os="windows"
            echo "${os}-${arch}"
            ;;
        *)
            error "Unsupported OS: $os" "Supported: macOS, Linux, Windows"
            return $ERR_UNSUPPORTED_PLATFORM
            ;;
    esac
}

# Pretty platform name for display
platform_pretty_name() {
    case "$1" in
        darwin-amd64)  echo "macOS (Intel)" ;;
        darwin-arm64)  echo "macOS (Apple Silicon)" ;;
        linux-amd64)   echo "Linux (x64)" ;;
        linux-arm64)   echo "Linux (ARM64)" ;;
        windows-amd64) echo "Windows (x64)" ;;
        *) echo "$1" ;;
    esac
}

# =============================================================================
# VERSION MANAGEMENT
# =============================================================================

get_manifest_version() {
    local manifest="${SCRIPT_DIR}/../manifest.json"
    if [[ -f "$manifest" ]]; then
        grep -o '"version":\s*"[^"]*"' "$manifest" | cut -d'"' -f4 | head -1 && return 0
    fi

    local marketplace="${SCRIPT_DIR}/../../../.claude-plugin/marketplace.json"
    if [[ -f "$marketplace" ]]; then
        grep -A 20 '"name": "md2wechat"' "$marketplace" | \
            grep -o '"version":\s*"[^"]*"' | cut -d'"' -f4 | head -1 && return 0
    fi
    return 1
}

get_cached_version() {
    if [[ -f "$VERSION_FILE" ]]; then
        grep -o '"version":\s*"[^"]*"' "$VERSION_FILE" | cut -d'"' -f4 | head -1
    fi
}

save_version_info() {
    local version=$1 platform=$2
    mkdir -p "$(dirname "$VERSION_FILE")"
    cat > "$VERSION_FILE" << EOF
{
  "version": "$version",
  "platform": "$platform",
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
}

# =============================================================================
# SYSTEM DEPENDENCY CHECK
# =============================================================================

check_download_tool() {
    if command -v curl &>/dev/null; then
        echo "curl"
    elif command -v wget &>/dev/null; then
        echo "wget"
    else
        return 1
    fi
}

# =============================================================================
# BINARY DOWNLOAD
# =============================================================================

# Download URLs in priority order (fallback chain)
get_download_urls() {
    local version=$1
    local bin_name=$2

    # 1. GitHub (primary)
    echo "${RELEASE_URL}/v${version}/${bin_name}"

    # 2. jsDelivr CDN (China-friendly, uses GitHub as backend)
    echo "https://cdn.jsdelivr.net/gh/${REPO}@v${version}/bin/${bin_name}"
}

download_binary() {
    local platform=$1 version=$2 binary_path=$3
    local bin_name="${BINARY_NAME}-${platform}"
    [[ "$platform" == windows-* ]] && bin_name="${bin_name}.exe"

    # Use cache directory for temp file (avoids /tmp noexec issues)
    local temp_dir="${CACHE_HOME}/tmp"
    mkdir -p "$temp_dir" 2>/dev/null || {
        error "Cannot create cache directory: $CACHE_HOME" \
            "Please check permissions or set XDG_CACHE_HOME."
        return $ERR_CACHE_DIR
    }
    local temp_file="${temp_dir}/${bin_name}.tmp"

    info "Downloading v${version} for $(platform_pretty_name "$platform")..."

    local tool
    tool=$(check_download_tool) || {
        show_missing_tool_help
        return $ERR_NO_DOWNLOAD_TOOL
    }

    # Try each mirror in order
    local urls
    urls=$(get_download_urls "$version" "$bin_name")

    local attempt=1
    local total_urls=0
    while IFS= read -r url; do
        ((total_urls++))
    done <<< "$urls"

    while IFS= read -r url; do
        if [[ -n "$url" ]]; then
            if [[ $attempt -gt 1 ]]; then
                info "Trying mirror $((attempt))/$total_urls..."
            fi

            local exit_code=0
            if [[ "$tool" == "curl" ]]; then
                curl -fsSL --max-time 120 --connect-timeout 10 \
                    -o "$temp_file" "$url" 2>/dev/null
                exit_code=$?
            else
                wget -q -O "$temp_file" --timeout=120 "$url" 2>/dev/null
                exit_code=$?
            fi

            if [[ $exit_code -eq 0 ]]; then
                # Validate downloaded file size
                local file_size=0
                file_size=$(wc -c < "$temp_file" 2>/dev/null) || file_size=0

                if [[ $file_size -ge $MIN_BINARY_SIZE ]]; then
                    mv "$temp_file" "$binary_path"
                    chmod +x "$binary_path" 2>/dev/null || true
                    save_version_info "$version" "$platform"
                    success "Ready! (cached for next time)"
                    return 0
                fi
            fi

            rm -f "$temp_file"
            ((attempt++))
        fi
    done <<< "$urls"

    return $ERR_DOWNLOAD_FAILED
}

# =============================================================================
# ERROR HELPERS - User-friendly guidance
# =============================================================================

show_missing_tool_help() {
    local os=$(uname -s | tr '[:upper:]' '[:lower:]')

    error "Need curl or wget to download" \
        "" \
        "Install one of these:" \
        "$([[ "$os" == "darwin" ]] && echo "  brew install curl" || echo "  sudo apt install curl    # Debian/Ubuntu" \
                                                          "  sudo yum install curl    # CentOS/RHEL")" \
        "" \
        "Then try again."
}

show_download_failed_help() {
    local platform=$1 version=$2
    local platform_name
    platform_name=$(platform_pretty_name "$platform")

    error "Download failed" \
        "" \
        "Possible reasons:" \
        "  • No internet connection" \
        "  • Version v${version} not released for ${platform_name}" \
        "  • Firewall blocking GitHub" \
        "" \
        "Quick fixes:" \
        "  • Check your network and retry" \
        "  • Download manually: https://github.com/${REPO}/releases" \
        "  • Report issue: https://github.com/${REPO}/issues"
}

show_cache_dir_error_help() {
    error "Cannot create cache directory" \
        "" \
        "Could not create: $CACHE_HOME" \
        "" \
        "Try one of these:" \
        "  • Check you have permission to create this directory" \
        "  • Set XDG_CACHE_HOME to a writable location:" \
        "      export XDG_CACHE_HOME=/tmp/.cache" \
        "  • Or manually download the binary"
}

show_version_error_help() {
    error "Version information not found" \
        "" \
        "This shouldn't happen. Please report:" \
        "https://github.com/${REPO}/issues"
}

# =============================================================================
# BINARY PROVISIONING
# =============================================================================

ensure_binary() {
    local platform version
    platform=$(detect_platform) || return $?

    local cached_binary="${BIN_DIR}/${BINARY_NAME}-${platform}"
    [[ "$platform" == windows-* ]] && cached_binary="${cached_binary}.exe"

    # Check cached binary (fast path - silent)
    if [[ -x "$cached_binary" ]]; then
        version=$(get_manifest_version)
        local cached_version
        cached_version=$(get_cached_version)

        if [[ "$version" == "$cached_version" ]] && [[ -n "$version" ]]; then
            echo "$cached_binary"
            return 0
        fi
    fi

    # Try local bin directory (development/offline fallback)
    local local_binary="${SCRIPT_DIR}/bin/${BINARY_NAME}-${platform}"
    [[ "$platform" == windows-* ]] && local_binary="${local_binary}.exe"

    if [[ -x "$local_binary" ]]; then
        echo "$local_binary"
        return 0
    fi

    # Need to download
    version=$(get_manifest_version)

    if [[ -z "$version" ]]; then
        show_version_error_help
        return 1
    fi

    mkdir -p "$BIN_DIR" 2>/dev/null || {
        show_cache_dir_error_help
        return $ERR_CACHE_DIR
    }

    if download_binary "$platform" "$version" "$cached_binary"; then
        echo "$cached_binary"
        return 0
    fi

    # Download failed - show contextual error
    local exit_code=$?
    case $exit_code in
        $ERR_CACHE_DIR)
            show_cache_dir_error_help
            ;;
        $ERR_NO_DOWNLOAD_TOOL)
            # Already shown in download_binary
            ;;
        *)
            show_download_failed_help "$platform" "$version"
            ;;
    esac
    return 1
}

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

main() {
    local binary
    binary=$(ensure_binary) || exit $?

    exec "$binary" "$@"
}

main "$@"
