# 경기도 메인 페이지 (/)
import json
from .site import PHONE, PHONE_DISPLAY, BASE_URL
from .data import REGION_GROUPS, CITIES
from .components import price_table, faq_block, faq_schema, byline
from .pages import (city_link, life_link, station_link, CITY_SHORT,
                    LIFE_PATH, LIFE_BY_NAME, STATION_BY_NAME, STATION_PATH, _cards)

DESC = "경기도 출장마사지·홈타이 예약 전 수원·분당·용인·부천·일산·안산·평택 생활권을 확인하세요."

_HERO = """<div class="hero">
  <div class="hero-content">
    <div class="hero-badge">전지역 방문 관리 · 연중무휴 24시간</div>
    <h1 class="hero-title">경기도 출장마사지<br><span class="hero-accent">전지역 홈타이</span><br>예약 안내</h1>
    <p class="hero-lead">수원, 성남, 용인, 고양, 부천, 안산, 안양, 화성, 평택, 남양주, 김포, 의정부 등 주요 지역별 방문 가능 지역과 예약 전 확인사항을 안내합니다.</p>
    <div class="hero-cta">
      <a href="#cities" class="btn btn-primary">시·군 찾기</a>
      <a href="#stations" class="btn btn-secondary">지하철역 찾기</a>
      <a href="#life" class="btn btn-secondary">생활권 찾기</a>
      <a href="/reservation/" class="btn btn-secondary">예약 안내 보기</a>
      <a href="/check/" class="btn btn-secondary">이용 전 확인사항</a>
    </div>
  </div>
  <div class="hero-stats">
    <div class="stat"><div class="stat-number">31</div><div class="stat-label">시·군 안내</div></div>
    <div class="stat"><div class="stat-number">2</div><div class="stat-label">권역 허브</div></div>
    <div class="stat"><div class="stat-number">80+</div><div class="stat-label">역세권 안내</div></div>
    <div class="stat"><div class="stat-number">24H</div><div class="stat-label">상담 가능</div></div>
  </div>
</div>"""


def _city_card(slug):
    c = CITIES[slug]
    return (f"/{slug}/", c["name"], "·".join(c["life"][:3]) + " 생활권")


def _build_main():
    south = REGION_GROUPS["south"]["cities"]
    north = REGION_GROUPS["north"]["cities"]

    # 권역 카드
    region_cards = _cards([
        ("/south/", "경기남부",
         ", ".join(CITY_SHORT[c] for c in south[:7]) + " 등 21개 시·군"),
        ("/north/", "경기북부",
         ", ".join(CITY_SHORT[c] for c in north[:7]) + " 등 10개 시·군"),
    ])

    city_cards = _cards([_city_card(s) for s in list(CITIES.keys())])

    # 핵심 생활권 카드
    key_life = ["수원역·인계동", "분당·판교", "동탄신도시", "일산·킨텍스",
                "부천역·상동", "안산중앙·초지", "남양주·다산", "하남·미사"]
    life_cards = _cards([(LIFE_PATH[LIFE_BY_NAME[n]], n, "생활권별 방문 가능 지역") for n in key_life])

    # 핵심 역 카드
    key_st = ["수원역", "판교역", "정자역", "기흥역", "부천역", "범계역", "의정부역", "대화역"]
    st_cards = _cards([(STATION_PATH[STATION_BY_NAME[n]], n, None) for n in key_st])

    faqs = [
        ("경기도 전 지역으로 방문이 가능한가요?",
         "네. 수원, 성남, 용인, 고양, 부천, 안산, 안양, 화성, 평택, 남양주, 김포, 의정부 등 "
         "경기도 31개 시·군 전 지역으로 방문 가능합니다. 외곽 지역은 차량 이동 기준과 추가 이동비를 "
         "예약 시 확인해 드립니다."),
        ("일반구가 있는 도시는 어떻게 찾나요?",
         "수원·용인·성남·부천·안산·안양·고양은 시 전체 페이지 아래 일반구 페이지가 있고, 그 아래 "
         "대표 동 생활권으로 연결됩니다. 시 → 구 → 동 순서로 찾으면 됩니다."),
        ("환승역은 노선별로 나뉘어 있나요?",
         "아니요. 금정역, 기흥역, 정자역 같은 환승역도 역명 기준 한 페이지로 안내하며 출구별로 "
         "나누지 않습니다."),
        ("외곽 읍·면 지역도 예약할 수 있나요?",
         "네. 양평, 가평, 연천, 포천, 안성 같은 외곽 지역도 가능하며, 차량 이동 기준·추가 이동비·"
         "방문 가능 주소를 미리 확인하면 예약이 수월합니다."),
        ("요금은 어떻게 정해지나요?",
         "60·90·120분 코스 기준 기본 요금이 있으며, 방문 지역과 시간대, 이동 거리에 따라 통화 시 "
         "최종 금액이 확정됩니다. 자세한 내용은 요금 안내를 확인하세요."),
    ]

    body = f"""
<section id="criteria">
  <h2>경기도에서 출장마사지를 찾을 때 먼저 확인할 기준</h2>
  <p>경기도는 서울보다 면적이 넓고 도시별 검색 의도와 이동 기준이 다릅니다. 수원, 성남, 안양, 부천, 광명은 역세권과 도심 생활권 중심으로, 용인, 화성, 남양주, 김포, 파주는 신도시와 읍·면 생활권이 함께 섞여 있습니다. 양평, 가평, 연천, 포천, 안성 같은 군·외곽 지역은 역세권보다 차량 이동 기준과 추가 이동비 확인이 더 중요합니다.</p>
  <p>그래서 이 사이트는 경기도 메인, {city_link('suwon')}·{city_link('seongnam')} 같은 시·군 안내, 일반구 안내, 읍·면·동 안내, 지하철역 안내, 생활권 안내로 구조를 나누어 안내합니다. 본인 위치가 어느 시·군의 어느 생활권에 속하는지 먼저 확인한 뒤, 가장 가까운 역이나 생활권을 기준으로 예약하면 이동 시간을 줄일 수 있습니다.</p>
  <p>모든 방문은 자택·숙소·오피스텔·호텔 등 다양한 장소에 대응하며, 건전한 방문 관리 서비스만 제공합니다. 예약 전에는 <a href="/check/">이용 전 확인사항</a>과 <a href="/reservation/">예약 안내</a>를 먼저 확인하세요.</p>
</section>

<section id="regions">
  <h2>경기남부·경기북부 권역별 안내</h2>
  <p>경기도는 크게 경기남부와 경기북부 두 권역으로 나뉩니다. 권역 페이지는 시·군 안내로 연결되는 허브입니다.</p>
  {region_cards}
</section>

<section id="cities">
  <h2>경기도 31개 시·군별 방문 가능 지역 안내</h2>
  <p>각 시·군 페이지에서 대표 생활권, 가까운 역, 일반구·대표 동, 예약 전 확인사항을 확인할 수 있습니다.</p>
  {city_cards}
</section>

<section id="stations">
  <h2>경기도 주요 지하철역별 안내</h2>
  <p>역명 기준으로 인접 시·군과 생활권을 연결해 안내합니다. 환승역도 역명 기준 한 페이지로 안내합니다.</p>
  {st_cards}
</section>

<section id="life">
  <h2>경기도 생활권별 예약 기준</h2>
  <p>생활권 페이지는 시·군, 읍·면·동, 역세권을 연결하는 허브입니다.</p>
  {life_cards}
</section>

<section id="check">
  <h2>경기도 홈타이 예약 전 확인사항</h2>
  <p>예약을 진행하기 전에 다음 항목을 먼저 확인하면 예약 과정이 훨씬 수월합니다.</p>
  <ul>
    <li><strong>방문 가능 주소 확인</strong> — 자택·숙소·오피스텔·호텔 등 정확한 주소와 건물 유형</li>
    <li><strong>예약 가능 시간 확인</strong> — 희망 시간대의 방문 가능 여부</li>
    <li><strong>추가 이동비 여부 확인</strong> — 기본 이동권 범위와 외곽 추가 비용</li>
    <li><strong>건물 출입 방식 확인</strong> — 공동현관·경비·주차 등</li>
    <li><strong>외곽·차량 이동 가능 여부 확인</strong> — 군·읍·면 지역 차량 진입 기준</li>
    <li><strong>결제·예약 변경 기준 확인</strong> — 결제 수단과 변경·취소 절차</li>
    <li><strong>개인정보 처리 기준 확인</strong> — 수집·이용·보관 방식</li>
    <li><strong>불법·선정적 서비스 불가 안내</strong> — 건전한 관리 서비스만 제공</li>
  </ul>
</section>

{byline()}

{price_table()}

{faq_block(faqs, "경기도 출장마사지 자주 묻는 질문")}
"""

    base = BASE_URL.rstrip("/")
    canonical = base + "/"
    webpage = {
        "@context": "https://schema.org", "@type": "WebPage",
        "name": "경기도 출장마사지｜수원·분당·용인·부천·일산 홈타이 지역 안내",
        "description": DESC, "url": canonical, "inLanguage": "ko",
        "isPartOf": {"@id": base + "/#organization"},
        "publisher": {"@id": base + "/#organization"},
    }
    _ld = lambda o: ('<script type="application/ld+json">\n'
                     + json.dumps(o, ensure_ascii=False, indent=2) + "\n</script>\n")
    extra = _ld(webpage) + faq_schema(faqs)

    return {
        "path": "",
        "title": "경기도 출장마사지｜수원·분당·용인·부천·일산 홈타이 지역 안내",
        "desc": DESC,
        "h1": "경기도 출장마사지 · 경기 전지역 홈타이 예약 안내",
        "hero": _HERO,
        "breadcrumb": [],
        "extra_head": extra,
        "body": body,
    }


PAGE = _build_main()
