#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 — 빙·네이버·얀덱스·Seznam 동시 통보.

사용법:
  python3 tools/indexnow.py                # sitemap.xml 의 모든 URL 통보(첫 일괄 통보)
  python3 tools/indexnow.py https://.../suwon/   https://.../bucheon/   # 특정 URL만 통보

글을 새로 올리거나 수정할 때마다 해당 URL을 인자로 넘기면 즉시 색인 통보됩니다.
(구글은 IndexNow 미참여 — 구글은 GSC 또는 tools/google_indexing.py 사용)
"""
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

BASE = BASE_URL.rstrip("/")
HOST = re.sub(r"^https?://", "", BASE).split("/")[0]
ENDPOINT = "https://api.indexnow.org/indexnow"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def urls_from_sitemap():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    return re.findall(r"<loc>([^<]+)</loc>", open(path, encoding="utf-8").read())


def submit(url_list):
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE}/{INDEXNOW_KEY}.txt",
        "urlList": url_list,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, resp.read().decode("utf-8", "ignore")


def main():
    url_list = sys.argv[1:] or urls_from_sitemap()
    if not url_list:
        sys.exit("통보할 URL 이 없습니다.")
    # IndexNow 는 요청당 최대 10,000 URL
    for i in range(0, len(url_list), 10000):
        chunk = url_list[i:i + 10000]
        status, body = submit(chunk)
        print(f"[IndexNow] {len(chunk)} URL 통보 → HTTP {status} {body or '(OK)'}")
    print(f"완료: 총 {len(url_list)} URL (host={HOST})")
    print("→ 빙·네이버·얀덱스에 즉시 전달됩니다. 구글은 GSC/색인 API를 사용하세요.")


if __name__ == "__main__":
    main()
