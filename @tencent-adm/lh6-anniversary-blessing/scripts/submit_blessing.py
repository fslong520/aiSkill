#!/usr/bin/env python3
"""Upload one blessing and render the final Lightlottery customer Markdown.

The script is intentionally UIN/OAuth-free.  Browser login and EntryToken
consumption are owned by the activity page.
"""

import argparse
import base64
import json
import mimetypes
import re
import secrets
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse


API_BASE = "https://lightmake.studio"
FRONTEND_ACTIVITY_BASE = "https://lighthouse6.cloud.tencent.com"
CAMPAIGN_EVENT_ID = "lh-6th-2026"
MAX_IMAGE_BYTES = 5 * 1024 * 1024
INVITE_RE = re.compile(r"^LH6-[A-Z0-9]{6}$")
SAFE_UNAVAILABLE = "活动入口暂时打不开，请稍后再试一次。"
INVALID_INVITE = "邀请码有误，请检查后重新提供。"


def render_customer_result(claim_url):
    return f"""祝福已送达。
登录腾讯云账号，即可解锁 1 次送祝福抽奖机会，在活动页实时开奖：
[进入活动页登录腾讯云账号，领取抽奖机会]({claim_url})
分享抽奖：邀请好友有效参与，即可获得分享抽奖资格
每邀请 1 位增加 1 份抽奖份额，最多 10 份
分享抽奖开奖时间：2026 年 9 月 16 日晚 20:00
抽奖随机抽取，以实际抽奖结果为准。
——— [六周年活动福利](https://cloud.tencent.com/act/pro/lh6th) ———
续费低至 1 折，拼团成功再送 1 或 3 个月时长。
新购低至 4.5 折，拼团成功再送 3 个月时长。
境内 2核4G5M、2核4G6M 可免费升配至 4核4G。
具体权益以官方活动页为准，最终解释权归主办方所有。"""


def post(path, payload, timeout, request_id):
    request = urllib.request.Request(
        API_BASE + path,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Idempotency-Key": request_id,
            "User-Agent": "lh6-anniversary-blessing/1.13.12",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read(65537)
        if len(raw) > 65536:
            raise ValueError("response too large")
    payload = json.loads(raw.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("response must be an object")
    return payload


def claim_url_from_response(payload):
    claim_url = str(payload.get("claim_url") or payload.get("ClaimUrl") or "").strip()
    if not claim_url:
        raise ValueError("missing claim_url")
    parsed = urlparse(claim_url)
    if parsed.scheme != "https" or parsed.hostname != urlparse(FRONTEND_ACTIVITY_BASE).hostname:
        raise ValueError("unexpected claim URL")
    # The Go service currently uses ?e=<signed EntryToken>.  Do not log or
    # decode it; the landing page consumes and clears it.
    if not parsed.query or "e=" not in parsed.query:
        raise ValueError("claim URL has no entry token")
    return claim_url


def normalize_inviter(value):
    value = str(value or "").strip().upper()
    if value and not INVITE_RE.fullmatch(value):
        raise ValueError("invalid inviter code")
    return value


def upload_ugc(args, source_id, request_id):
    """Best-effort UGC upload.  Any failure is deliberately ignored."""
    try:
        if args.text:
            ugc = {
                "SourceId": source_id,
                "Kind": args.kind,
                "Text": args.text,
                "PublicConsent": bool(args.public_consent),
            }
            post("/ugc/blessings", ugc, 10, request_id)
            return

        content_type, _ = mimetypes.guess_type(args.image_file)
        if content_type not in ("image/png", "image/jpeg", "image/webp"):
            return
        with open(args.image_file, "rb") as image_file:
            content = image_file.read(MAX_IMAGE_BYTES + 1)
        if len(content) > MAX_IMAGE_BYTES:
            return
        image = post(
            "/ugc/images",
            {
                "SourceId": source_id,
                "ContentType": content_type,
                "ImageBase64": base64.b64encode(content).decode("ascii"),
            },
            30,
            request_id,
        )
        image_url = str(image.get("ImageUrl") or image.get("image_url") or "").strip()
        if not image_url:
            return
        post(
            "/ugc/blessings",
            {
                "SourceId": source_id,
                "Kind": args.kind,
                "ImageUrl": image_url,
                "PublicConsent": bool(args.public_consent),
            },
            10,
            request_id,
        )
    except (OSError, KeyError, TypeError, ValueError, urllib.error.HTTPError,
            urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return


def main():
    parser = argparse.ArgumentParser(description="Submit a Lighthouse anniversary blessing")
    parser.add_argument("--text")
    parser.add_argument("--image-file")
    parser.add_argument("--invite-code", default="")
    parser.add_argument("--source-id", default="")
    parser.add_argument("--public-consent", action="store_true")
    parser.add_argument("--kind", default="自由祝福", help="祝福墙分类；不限制为固定枚举")
    # Product v1.13.5 passes these context fields.  The current /entry API
    # intentionally only persists EventId/SourceId/InviteCode.
    parser.add_argument("--story-choice", default="")
    parser.add_argument("--blessing-type", default="")
    parser.add_argument("--source", default="skillhub")
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args()

    if bool(args.text) == bool(args.image_file):
        parser.error("provide exactly one of --text or --image-file")
    try:
        inviter_code = normalize_inviter(args.invite_code)
    except ValueError:
        print(INVALID_INVITE)
        return 2

    source_id = args.source_id.strip() or "skill-" + secrets.token_urlsafe(18)
    request_id = secrets.token_urlsafe(18)
    timeout = max(1.0, min(args.timeout, 30.0))

    # Product flow requires blessing delivery before activity-flow creation.
    upload_ugc(args, source_id, request_id)
    try:
        entry = post(
            "/entry",
            {
                "EventId": CAMPAIGN_EVENT_ID,
                "SourceId": source_id,
                "InviteCode": inviter_code,
            },
            timeout,
            request_id,
        )
        print(render_customer_result(claim_url_from_response(entry)))
        return 0
    except (urllib.error.HTTPError, urllib.error.URLError, OSError, TimeoutError,
            UnicodeError, ValueError, TypeError, json.JSONDecodeError):
        print(SAFE_UNAVAILABLE)
        return 2


if __name__ == "__main__":
    sys.exit(main())
