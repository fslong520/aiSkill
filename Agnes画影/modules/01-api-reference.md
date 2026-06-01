# API 参考

## 通用 curl 骨架

```bash
curl -s https://apihub.agnes-ai.com/v1/{ENDPOINT} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -d '{...}'
```

## 模型差异

| 能力 | 端点 | 模型名 | 关键参数 | 结果提取 |
|------|------|--------|---------|---------|
| 文本 | `chat/completions` | `agnes-2.0-flash` | `messages`, `max_tokens` | `.choices[0].message.content` |
| 图片 | `images/generations` | `agnes-image-2.0-flash` | `prompt`, `n`, `size` | `.data[0].url` |
| 视频 | `video/generations` | `agnes-video-v2.0` | `prompt`, `duration`, `size` | 异步轮询（见下） |

## 图片参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `prompt` | 图片描述（中/英） | 必填 |
| `n` | 生成张数 | 1 |
| `size` | 尺寸 | `1024x1024` |
| `model` | 模型名 | `agnes-image-2.0-flash` |

## 视频参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `prompt` | 视频描述 | 必填 |
| `duration` | 时长（秒），支持 5~30 | 5 |
| `size` | 尺寸 | `1280x768` |
| `model` | 模型名 | `agnes-video-v2.0` |

## 视频轮询

```bash
# 提交
TASK_ID=$(curl -s https://apihub.agnes-ai.com/v1/video/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -d '{"model":"agnes-video-v2.0","prompt":"...","duration":5}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('task_id',''))")

# 轮询（间隔 10-15 秒）
while true; do
  resp=$(curl -s "https://apihub.agnes-ai.com/v1/video/generations/$TASK_ID" \
    -H "Authorization: Bearer $AGNES_API_KEY")
  status=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('status',''))")
  progress=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('progress',0))")
  echo "[$progress%] $status"
  [ "$status" = "completed" ] && break
  [ "$status" = "failed" ] && echo "FAILED" && break
  sleep 12
done

# 取结果
url=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin).get('data',{}); print(d.get('remixed_from_video_id') or d.get('url') or '')")
echo "视频 URL: $url"
```

## 文本参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `messages` | 对话消息数组 | 必填 |
| `max_tokens` | 最大生成长度 | 2048 |
| `model` | 模型名 | `agnes-2.0-flash` |
