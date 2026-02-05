# 微信公众号 API 参考

## SDK 使用

使用 `github.com/silenceper/wechat/v2` SDK。

```go
import (
    "github.com/silenceper/wechat/v2"
    "github.com/silenceper/wechat/v2/officialaccount/config"
    "github.com/silenceper/wechat/v2/officialaccount/material"
    "github.com/silenceper/wechat/v2/officialaccount/draft"
)
```

## 初始化

```go
// 创建微信实例
wc := wechat.NewWechat()

// 配置缓存（必需）
memory := cache.NewMemory()

// 配置公众号参数
cfg := &config.Config{
    AppID:     appID,
    AppSecret: appSecret,
    Cache:     memory,
}

// 获取公众号实例
officialAccount := wc.GetOfficialAccount(cfg)
```

## API 1: 上传永久素材

上传图片到微信素材库，返回 media_id 和 URL。

### 调用方式

```bash
md2wechat upload_image <file_path>
md2wechat download_and_upload <url>
```

### Go 实现

```go
// 获取素材管理器
materialManager := officialAccount.GetMaterial()

// 上传永久素材
mediaID, url, err := materialManager.AddMaterial(
    material.MediaTypeImage,  // 素材类型
    file,                       // *os.File 或 io.Reader
)
```

### 响应格式

```json
{
  "success": true,
  "media_id": "media_id_xxx",
  "wechat_url": "https://mmbiz.qpic.cn/mmbiz_jpg/xxx/0?wx_fmt=jpeg"
}
```

### 错误码

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 40001 | AppID 错误 | 检查配置 |
| 40004 | 文件为空 | 检查文件路径 |
| 40005 | 文件类型不支持 | 检查图片格式 |
| 40006 | 文件大小超限 | 压缩图片 |
| 42001 | AppSecret 错误 | 检查配置 |

## API 2: 新建草稿

创建图文草稿到公众号草稿箱。

### 调用方式

```bash
md2wechat create_draft <json_file>
```

### Go 实现

```go
// 获取草稿管理器
draftManager := officialAccount.GetDraft()

// 构建文章
articles := []draft.Article{
    {
        Title:            "文章标题",
        Author:           "作者",
        Digest:           "摘要（120字符）",
        Content:          "<!DOCTYPE html><html>...</html>",
        ThumbMediaID:     "封面图的 media_id",
        ShowCoverPic:     1,  // 是否显示封面图
        ContentSourceURL: "原文链接",
    },
}

// 创建草稿
mediaID, err := draftManager.AddDraft(articles)
```

### 响应格式

```json
{
  "success": true,
  "media_id": "draft_media_id_xxx",
  "draft_url": "https://mp.weixin.qq.com/..."
}
```

### 文章字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Title | string | 是 | 标题，不超过 64 字符 |
| Author | string | 否 | 作者 |
| Digest | string | 否 | 摘要，不超过 120 字符 |
| Content | string | 是 | HTML 正文 |
| ThumbMediaID | string | 是 | 封面图 media_id |
| ShowCoverPic | int | 否 | 是否显示封面，0 或 1 |
| ContentSourceURL | string | 否 | 原文链接 |

## 认证配置

### 环境变量

```bash
export WECHAT_APPID="your_appid"
export WECHAT_SECRET="your_secret"
```

### Go 代码读取

```go
func loadConfig() (*Config, error) {
    return &Config{
        AppID:     os.Getenv("WECHAT_APPID"),
        AppSecret: os.Getenv("WECHAT_SECRET"),
    }, nil
}
```

## 图片生成 API

使用兼容 OpenAI DALL-E 的 API。

### 配置

```bash
export IMAGE_API_KEY="your_api_key"
export IMAGE_API_BASE="https://api.example.com/v1"
```

### 调用

```go
// 生成图片
type ImageAPIRequest struct {
    Prompt string `json:"prompt"`
    Size   string `json:"size"` // 1024x1024
    N      int    `json:"n"`    // 1
}

type ImageAPIResponse struct {
    Data []struct {
        URL string `json:"url"`
    } `json:"data"`
}

// POST /images/generations
```

### 错误处理

| 错误 | 处理方式 |
|------|----------|
| API Key 无效 | 返回错误，提示检查配置 |
| 配额超限 | 返回错误，提示稍后重试 |
| 生成失败 | 返回错误，跳过该图片 |
| 超时 | 重试 1 次，仍失败则跳过 |

## 最佳实践

### 1. 并发限制

微信公众号 API 有调用频率限制：

| API | 限制 |
|-----|------|
| 上传素材 | 100 次/天 |
| 创建草稿 | 100 次/天 |

建议：
- 批量处理时控制并发数
- 失败后等待 1 秒再重试

### 2. 缓存策略

```go
// 缓存已上传的图片，避免重复上传
type ImageCache struct {
    sync.RWMutex
    cache map[string]string // localPath -> mediaID
}

func (c *ImageCache) Get(path string) (string, bool) {
    c.RLock()
    defer c.RUnlock()
    id, ok := c.cache[path]
    return id, ok
}

func (c *ImageCache) Set(path, id string) {
    c.Lock()
    defer c.Unlock()
    c.cache[path] = id
}
```

### 3. 错误重试

```go
func retry(fn func() error, maxAttempts int) error {
    var err error
    for i := 0; i < maxAttempts; i++ {
        err = fn()
        if err == nil {
            return nil
        }
        time.Sleep(time.Second)
    }
    return err
}
```

### 4. 日志记录

```go
type Logger struct {
    *zap.Logger
}

func (l *Logger) LogUpload(filePath string, mediaID, url string, duration time.Duration) {
    l.Info("image uploaded",
        zap.String("file", filePath),
        zap.String("media_id", maskMediaID(mediaID)),
        zap.String("url", url),
        zap.Duration("duration", duration),
    )
}

func maskMediaID(id string) string {
    if len(id) < 8 {
        return "***"
    }
    return id[:4] + "***" + id[len(id)-4:]
}
```

## 完整调用示例

```go
package main

import (
    "fmt"
    "os"
    "github.com/silenceper/wechat/v2"
    "github.com/silenceper/wechat/v2/cache"
    "github.com/silenceper/wechat/v2/officialaccount/config"
    "github.com/silenceper/wechat/v2/officialaccount/material"
    "github.com/silenceper/wechat/v2/officialaccount/draft"
)

func main() {
    // 1. 初始化
    wc := wechat.NewWechat()
    memory := cache.NewMemory()
    cfg := &config.Config{
        AppID:     os.Getenv("WECHAT_APPID"),
        AppSecret: os.Getenv("WECHAT_SECRET"),
        Cache:     memory,
    }
    oa := wc.GetOfficialAccount(cfg)

    // 2. 上传图片
    mat := oa.GetMaterial()
    file, _ := os.Open("image.jpg")
    defer file.Close()
    mediaID, url, _ := mat.AddMaterial(material.MediaTypeImage, file)
    fmt.Printf("Uploaded: %s, %s\n", mediaID, url)

    // 3. 创建草稿
    dm := oa.GetDraft()
    articles := []draft.Article{
        {
            Title:        "测试文章",
            Content:      "<p>正文内容</p>",
            ThumbMediaID: mediaID,
            ShowCoverPic: 1,
        },
    }
    draftID, _ := dm.AddDraft(articles)
    fmt.Printf("Draft: %s\n", draftID)
}
```
