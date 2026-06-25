#!/usr/bin/env python3
"""구글 Indexing API 색인 통보 (구글은 IndexNow 미참여).

⚠️ 사전 준비 (1회):
  1) Google Cloud 콘솔에서 프로젝트 생성 → "Indexing API" 사용 설정
  2) 서비스 계정 생성 후 JSON 키 다운로드 → 경로를 GOOGLE_APPLICATION_CREDENTIALS 로 지정
  3) 구글 서치콘솔에서 해당 사이트 속성에 서비스 계정 이메일을
     "소유자(Owner)" 권한으로 추가
  4) pip install google-auth requests

참고: 구글 Indexing API는 공식적으로 JobPosting/BroadcastEvent 대상이지만,
일반 URL 통보에도 널리 쓰입니다. 가장 확실한 방법은 GSC + 사이트맵 제출입니다.

사용법:
  export GOOGLE_APPLICATION_CREDENTIALS=/path/service-account.json
  python3 tools/google_indexing.py                 # sitemap.xml 전체
  python3 tools/google_indexing.py https://.../suwon/   # 특정 URL
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def urls_from_sitemap():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    return re.findall(r"<loc>([^<]+)</loc>", open(path, encoding="utf-8").read())


def main():
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("의존성 필요: pip install google-auth requests")

    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path or not os.path.exists(cred_path):
        sys.exit("GOOGLE_APPLICATION_CREDENTIALS 환경변수에 서비스 계정 JSON 경로를 지정하세요.")

    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    session = AuthorizedSession(creds)

    url_list = sys.argv[1:] or urls_from_sitemap()
    ok = 0
    for url in url_list:
        r = session.post(ENDPOINT, json={"url": url, "type": "URL_UPDATED"})
        tag = "OK" if r.status_code == 200 else f"ERR {r.status_code}"
        if r.status_code == 200:
            ok += 1
        print(f"[{tag}] {url}")
        if r.status_code != 200:
            print("   ", r.text[:200])
    print(f"\n완료: {ok}/{len(url_list)} 성공")
    print("주의: 구글 Indexing API는 일 200건(쿼터) 제한이 있습니다.")


if __name__ == "__main__":
    main()
