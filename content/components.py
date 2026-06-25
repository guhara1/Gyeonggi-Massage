# 공통 컴포넌트 — 요금표(코스 카드), FAQ, 저자 바이라인, 권위 사이트 링크
import json
from .site import BRAND, BASE_URL, PHONE, PHONE_DISPLAY, EDITOR, EDITOR_ROLE

_BASE = BASE_URL.rstrip("/")
LAST_UPDATED = "2026-06-25"

# 시·군청 공식 홈페이지 (권위 있는 외부 링크 / E-E-A-T)
CITY_OFFICIAL = {
    "suwon": "https://www.suwon.go.kr/", "yongin": "https://www.yongin.go.kr/",
    "hwaseong": "https://www.hscity.go.kr/", "seongnam": "https://www.seongnam.go.kr/",
    "bucheon": "https://www.bucheon.go.kr/", "ansan": "https://www.ansan.go.kr/",
    "pyeongtaek": "https://www.pyeongtaek.go.kr/", "anyang": "https://www.anyang.go.kr/",
    "siheung": "https://www.siheung.go.kr/", "gimpo": "https://www.gimpo.go.kr/",
    "gwangju-si": "https://www.gjcity.go.kr/", "hanam": "https://www.hanam.go.kr/",
    "gwangmyeong": "https://www.gm.go.kr/", "gunpo": "https://www.gunpo.go.kr/",
    "osan": "https://www.osan.go.kr/", "icheon": "https://www.icheon.go.kr/",
    "anseong": "https://www.anseong.go.kr/", "uiwang": "https://www.uiwang.go.kr/",
    "yangpyeong": "https://www.yp21.go.kr/", "yeoju": "https://www.yeoju.go.kr/",
    "gwacheon": "https://www.gccity.go.kr/", "goyang": "https://www.goyang.go.kr/",
    "namyangju": "https://www.nyj.go.kr/", "paju": "https://www.paju.go.kr/",
    "uijeongbu": "https://www.ui4u.go.kr/", "yangju": "https://www.yangju.go.kr/",
    "guri": "https://www.guri.go.kr/", "pocheon": "https://www.pocheon.go.kr/",
    "dongducheon": "https://www.ddc.go.kr/", "gapyeong": "https://www.gp.go.kr/",
    "yeoncheon": "https://www.yeoncheon.go.kr/",
}

# 코스별 요금 데이터 (요청 이미지 기준)
COURSES = [
    ("60분 코스", "90,000", "60분", "핵심 부위 위주 가벼운 이완", False),
    ("90분 코스", "150,000", "90분", "전신 균형 표준 구성·아로마 포함", True),
    ("120분 코스", "180,000", "120분", "구석구석 집중하는 프리미엄 구성", False),
]


def price_table(scope_label="기본 요금"):
    """코스 시간 기준 요금표. class='pricing'으로 감싸 본문 글자수 측정에서 제외된다."""
    cards = []
    for name, price, mins, desc, featured in COURSES:
        cls = "course-card is-featured" if featured else "course-card"
        badge = '<span class="course-badge">추천</span>' if featured else ""
        cards.append(
            f'<div class="{cls}">{badge}'
            f'<p class="course-name">{name}</p>'
            f'<p class="course-price">{price}<span>원</span></p>'
            f'<p class="course-time">{mins}</p>'
            f'<p class="course-desc">{desc}</p>'
            f'<a class="course-cta" href="tel:{PHONE}">예약 문의</a>'
            f'</div>'
        )
    return (
        '<section class="pricing course-pricing" aria-label="코스별 기본 요금">'
        '<div class="course-head">'
        f'<h2>코스 시간으로 보는 {scope_label}</h2>'
        '<p class="course-sub">관리 시간(60·90·120분)을 기준으로 정리한 기본 금액입니다. '
        '표시되지 않은 별도 비용은 두지 않는 것을 원칙으로 안내합니다.</p>'
        '</div>'
        f'<div class="course-grid">{"".join(cards)}</div>'
        '<p class="course-foot">방문 지역과 시간대, 이동 거리에 따라 최종 금액은 통화 시 확정됩니다. '
        '<a href="/pricing/">요금·예약 기준 자세히 보기 →</a></p>'
        '</section>'
    )


def faq_block(faqs, heading):
    """FAQ 본문(dl) HTML 생성. faqs = [(q, a), ...]"""
    rows = []
    for i, (q, a) in enumerate(faqs, 1):
        rows.append(f'<dt id="faq-{i}">{q}</dt><dd>{a}</dd>')
    return (
        f'<section id="faq"><h2>{heading}</h2>'
        f'<dl class="faq-list">{"".join(rows)}</dl></section>'
    )


def faq_schema(faqs):
    """FAQPage JSON-LD (extra_head 용)."""
    obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + "\n</script>\n")


def image_schema(name, caption):
    """ImageObject JSON-LD — 선호 썸네일 지정(og:image와 함께 사용)."""
    obj = {
        "@context": "https://schema.org",
        "@type": "ImageObject",
        "contentUrl": _BASE + "/assets/og-image.png",
        "url": _BASE + "/assets/og-image.png",
        "name": name,
        "caption": caption,
        "width": 1200,
        "height": 630,
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + "\n</script>\n")


def byline():
    """저자 바이라인 — E-E-A-T(누가, 어떻게, 왜) 신호."""
    return (
        '<section class="byline" id="about-this-guide">'
        '<h2>이 안내를 만든 사람과 기준</h2>'
        f'<p>이 페이지는 <strong>{EDITOR}</strong>({EDITOR_ROLE})가 직접 방문 예약을 받아 온 '
        '상담 경험을 바탕으로 작성하고 검수했습니다. 지역별 이동 기준, 추가 이동비, '
        '건물 출입 방식처럼 실제 예약 과정에서 자주 확인되는 항목을 중심으로 정리했습니다.</p>'
        '<p class="byline-meta">'
        f'<span>작성·검수: {EDITOR}</span>'
        f'<span>예약 문의: <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>'
        f'<span>최종 업데이트: {LAST_UPDATED}</span>'
        '</p>'
        '<p class="byline-note">건전한 방문 관리 서비스만 안내하며, 불법·선정적 요청에는 '
        '어떤 경우에도 응하지 않습니다. 요금·예약 기준은 통화 시 다시 확인됩니다.</p>'
        '</section>'
    )


def external_refs(city_slug, wiki_title):
    """권위 있는 외부 링크 — 위키백과 + 시·군청 공식 홈페이지."""
    wiki_url = "https://ko.wikipedia.org/wiki/" + wiki_title.replace(" ", "_")
    rows = [
        f'<li><a href="{wiki_url}" target="_blank" rel="noopener">위키백과 — {wiki_title} 지역 정보</a> '
        '에서 행정구역과 생활권 구성을 확인할 수 있습니다.</li>'
    ]
    official = CITY_OFFICIAL.get(city_slug)
    if official:
        rows.append(
            f'<li><a href="{official}" target="_blank" rel="noopener">{wiki_title} 공식 홈페이지</a> '
            '에서 행정 안내와 교통 정보를 확인할 수 있습니다.</li>'
        )
    return (
        '<section class="refs"><h2>참고 자료</h2>'
        '<p>방문 주소와 생활권을 확인할 때 함께 보면 좋은 공식·권위 자료입니다.</p>'
        f'<ul>{"".join(rows)}</ul></section>'
    )


def place_section(name):
    """방문 가능 장소 안내 — 장소별 준비 사항(본문 보강)."""
    return (
        f'<section class="places"><h2>{name} 방문 가능 장소</h2>'
        f'<p>{name} 지역으로는 자택, 오피스텔, 숙소, 호텔 등 다양한 장소로 방문 관리가 '
        '가능합니다. 아파트 단지는 단지명과 동·호수, 오피스텔·숙소는 건물명과 출입 방식, '
        '호텔은 호텔명과 객실 정보를 알려 주시면 방문이 한결 원활합니다.</p>'
        '<ul>'
        '<li><strong>자택·주택</strong> — 출입 방법과 주차 가능 여부 확인</li>'
        '<li><strong>오피스텔·숙소</strong> — 공동현관 비밀번호·출입 방식 확인</li>'
        '<li><strong>호텔</strong> — 호텔명·객실 정보 확인</li>'
        '</ul></section>'
    )


def reservation_note(short):
    """하단 예약 안내 문장 — 키워드는 여기서 자연스럽게 1회 사용."""
    return (
        '<section class="cta-note"><h2>예약 안내</h2>'
        f'<p>{short} 출장마사지·홈타이 방문 예약은 '
        f'<a href="tel:{PHONE}">{PHONE_DISPLAY}</a>(연중무휴 24시간 상담)로 문의하시면, '
        '방문 가능 지역과 시간, 추가 이동비 여부를 함께 확인해 드립니다. '
        '예약 전 <a href="/check/">이용 전 확인사항</a>과 '
        '<a href="/reservation/">예약 안내</a>를 먼저 확인하세요.</p></section>'
    )
