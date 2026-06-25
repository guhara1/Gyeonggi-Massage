# 바로 GO — 경기도 출장마사지·홈타이 안내 사이트

경기도 31개 시·군 전지역 방문 관리(출장마사지·홈타이) 안내를 위한 정적 사이트입니다.
구글 SEO 정책(E-E-A-T, 도움되는 콘텐츠, 구조화 데이터)에 맞춘 구조로 설계되었습니다.

## 구조

- **경기도 메인** `/gyeonggi/`
- **권역 허브** 경기남부 `/gyeonggi/south/`, 경기북부 `/gyeonggi/north/`
- **시·군** `/gyeonggi/{city}/` (31개)
- **일반구** `/gyeonggi/{city}/{gu}/` (20개)
- **읍·면·동** `/gyeonggi/{city}/{gu}/{dong}/` 또는 `/gyeonggi/{city}/{dong}/`
- **지하철역** `/gyeonggi/station/` 허브 + `/gyeonggi/station/{name}/` (역명 기준 1개 URL)
- **생활권** `/gyeonggi/life/` 허브 + `/gyeonggi/life/{slug}/`
- **정보** 예약 안내 `/reservation/`, 요금 `/pricing/`, 이용 가이드 `/guide/`,
  이용 전 확인사항 `/check/`, 고객센터 `/support/`, 개인정보처리방침 `/support/privacy/`
- 루트 `/` → `/gyeonggi/` 리다이렉트

## SEO 원칙 (적용 사항)

- 메뉴명·URL에 키워드("출장마사지")를 반복하지 않음 (영문 지역 slug만 사용)
- 메타 description 80자 이내
- 본문 1,500자 미만 페이지는 자동 `noindex` 처리 + sitemap 제외 (얇은 콘텐츠 방지)
- 환승역도 역명 기준 한 페이지, 출구별 페이지 없음
- 번호 동은 대표동·생활권으로 통합
- 외곽·군 지역은 차량 이동 기준·추가 이동비 안내 강조
- **구조화 데이터**: Organization, WebPage, BreadcrumbList, FAQPage, ImageObject
  (방문형이므로 LocalBusiness는 사용하지 않음)
- **E-E-A-T**: 책임 저자 바이라인, 작성·검수자·연락처·업데이트일 명시
- **권위 외부 링크**: 시·군별 위키백과·시·군청 공식 홈페이지
- 모든 페이지 내부링크(시·군 ↔ 구 ↔ 동 ↔ 역 ↔ 생활권) 연결

## 빌드

```bash
python3 build.py
```

`content/` 패키지의 페이지 정의를 읽어 저장소 루트에 정적 HTML, `sitemap.xml`,
`robots.txt`, 루트 리다이렉트를 생성합니다. (Cloudflare Pages가 저장소 루트를 그대로 배포)

### 데이터/콘텐츠 소스

- `content/site.py` — 상호(바로 GO)·전화·텔레그램 링크·내비게이션
- `content/data.py` — 31개 시·군 / 일반구 / 읍면동 / 지하철역 / 생활권 데이터
- `content/components.py` — 요금표(코스 카드)·FAQ·저자 바이라인·외부 참고링크
- `content/pages.py` — 시·군/구/동/역/생활권 페이지 생성기
- `content/main.py`, `content/info.py` — 메인·정보 페이지

## 확장 (2차·3차 색인)

`content/data.py`의 `DONG_PAGES`, `STATIONS`, `LIFE_AREAS`에 항목을 추가하면
페이지가 자동 생성됩니다. 실제 유입(GSC 데이터)을 확인하며 단계적으로 확장하세요.

## 색인(인덱싱) & 구조화 데이터

### 스키마 (모든 지역 페이지)
- `Organization`, `WebPage`(primaryImageOfPage), `BreadcrumbList`, `FAQPage`, `ImageObject`
- `Service` + `AggregateOffer`/`Offer` — 60·90·120분 코스 **가격** 포함
- `AggregateRating` + `Review` — **실제 후기 전용**. `content/reviews.py` 에 실제 후기를
  넣고 `ENABLE_REVIEWS = True` 로 바꾸면 자동 적용. (가짜 후기는 정책 위반·패널티 위험)

### 사이트맵 / RSS / robots
- `sitemap.xml` (lastmod·changefreq 포함), `rss.xml` (RSS 2.0, 사이트맵으로도 제출 가능)
- `robots.txt` — Googlebot·Yeti(네이버)·bingbot 명시 허용 + 사이트맵·RSS

### 가장 빠른 색인 통보
- **IndexNow** (빙·네이버·얀덱스 즉시 통보): 루트에 키 파일 `{KEY}.txt` 자동 생성
  - 첫 일괄 통보: `python3 tools/indexnow.py`
  - 글 올릴 때마다: `python3 tools/indexnow.py https://gyeonggi-massage.pages.dev/<경로>/`
- **구글**(IndexNow 미참여):
  - 권장: 구글 서치콘솔에 사이트 등록 + `sitemap.xml` 제출
  - 선택: `tools/google_indexing.py` (서비스 계정 필요, 일 200건 쿼터)
- **네이버**: 서치어드바이저 등록 + 사이트맵 제출 (IndexNow 로도 통보됨)
