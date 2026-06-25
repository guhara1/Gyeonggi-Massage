# 경기도 전 페이지 생성기 — 시·군 / 일반구 / 읍면동 / 지하철역 / 생활권
from .site import BRAND, PHONE, PHONE_DISPLAY
from .data import (REGION_GROUPS, CITIES, GU_DONG, CITY_DONG,
                   LIFE_AREAS, STATIONS, DONG_PAGES)
from .components import (price_table, faq_block, faq_schema, image_schema,
                         byline, external_refs, reservation_note, place_section)

# ---------- 조회용 인덱스 ----------
CITY_NAME = {s: c["name"] for s, c in CITIES.items()}
CITY_SHORT = {s: c["short"] for s, c in CITIES.items()}

STATION_BY_NAME = {name: slug for slug, name, *_ in STATIONS}
STATION_PATH = {slug: f"/station/{slug}/" for slug, *_ in STATIONS}
STATIONS_BY_CITY = {}
for _slug, _name, _city, *_rest in STATIONS:
    STATIONS_BY_CITY.setdefault(_city, []).append((_slug, _name))

LIFE_BY_NAME = {name: slug for slug, name, *_ in LIFE_AREAS}
LIFE_PATH = {slug: f"/life/{slug}/" for slug, *_ in LIFE_AREAS}
LIFE_BY_CITY = {}
for _slug, _name, _city, *_rest in LIFE_AREAS:
    LIFE_BY_CITY.setdefault(_city, []).append((_slug, _name))

# 동 경로 인덱스
DONG_PATH = {}      # slug -> path
DONG_NAME = {}      # slug -> name
DONG_BY_KEY = {}    # (city, name) -> (slug, path)
for _d in DONG_PAGES:
    _slug, _name, _city, _gu = _d[0], _d[1], _d[2], _d[3]
    _p = f"/{_city}/{_gu}/{_slug}/" if _gu else f"/{_city}/{_slug}/"
    DONG_PATH[_slug] = _p
    DONG_NAME[_slug] = _name
    DONG_BY_KEY[(_city, _name)] = (_slug, _p)


# ---------- 링크 헬퍼 ----------
def city_link(slug):
    return f'<a href="/{slug}/">{CITY_NAME[slug]}</a>'


def station_link(name):
    slug = STATION_BY_NAME.get(name)
    return f'<a href="{STATION_PATH[slug]}">{name}</a>' if slug else name


def life_link(name):
    slug = LIFE_BY_NAME.get(name)
    return f'<a href="{LIFE_PATH[slug]}">{name} 생활권</a>' if slug else f"{name} 생활권"


def dong_link(city, name):
    hit = DONG_BY_KEY.get((city, name))
    return f'<a href="{hit[1]}">{name}</a>' if hit else name


def _desc(text):
    """메타 설명 80자 이내 보장."""
    text = text.strip()
    return text if len(text) <= 80 else text[:77].rstrip() + "…"


def _cards(items):
    """items = [(href, title, sub)] → 카드 그리드."""
    cells = []
    for href, title, sub in items:
        sub_html = f"<p>{sub}</p>" if sub else ""
        cells.append(f'<a href="{href}" class="card"><h3>{title}</h3>{sub_html}'
                     f'<span class="card-arrow">→</span></a>')
    return f'<div class="card-grid">{"".join(cells)}</div>'


CHECK_LIST = (
    "<ul>"
    "<li><strong>방문 가능 주소 확인</strong> — 자택·숙소·오피스텔 등 정확한 주소와 건물 유형</li>"
    "<li><strong>예약 가능 시간 확인</strong> — 희망 시간대의 방문 가능 여부</li>"
    "<li><strong>추가 이동비 여부 확인</strong> — 기본 이동권 범위와 외곽 추가 비용</li>"
    "<li><strong>건물 출입 방식 확인</strong> — 공동현관·경비·주차 등</li>"
    "<li><strong>결제·예약 변경 기준 확인</strong> — 가능한 결제 수단과 변경·취소 절차</li>"
    "<li><strong>개인정보 처리 기준 확인</strong> — 수집·이용·보관 방식</li>"
    "<li><strong>불법·선정적 서비스 불가 안내</strong> — 건전한 관리 서비스만 제공</li>"
    "</ul>"
)


PAGES = []


# ========== 시·군 페이지 ==========
def build_city(slug, c):
    name, short, group = c["name"], c["short"], c["group"]
    grp = REGION_GROUPS[group]
    car = c.get("car", False)

    life_names = [n for _, n in LIFE_BY_CITY.get(slug, [])] or c["life"]
    st_names = [n for _, n in STATIONS_BY_CITY.get(slug, [])] or c["stations"]

    # intro 섹션
    move_line = (
        f"{short} 외곽·읍면 지역은 지하철역보다 차량 이동 기준과 추가 이동비, "
        "방문 가능 주소 확인이 더 중요합니다. 예약 전에 차량 진입과 주차 가능 여부를 함께 확인하세요."
        if car else
        f"{short}은 역세권과 신도시 생활권이 함께 발달해, 가장 가까운 역과 생활권을 기준으로 "
        "방문 주소를 정하면 이동 시간을 줄일 수 있습니다."
    )
    life_txt = ", ".join(c["life"][:5])
    near_txt = ", ".join(CITY_SHORT[n] for n in c["nearby"])

    body = [
        f'<section id="criteria"><h2>{short}에서 출장마사지를 찾을 때 먼저 확인할 기준</h2>',
        f"<p>{c['intro']}</p>",
        f"<p>{short}시는 경기{'남부' if group=='south' else '북부'}에 속하며, "
        f"대표 생활권으로는 {life_txt} 등이 있습니다. 같은 {short} 안에서도 도심 상권과 "
        f"신도시 주거지, 외곽 생활권의 이동 기준이 서로 다르기 때문에, 본인 위치가 어느 생활권에 "
        f"속하는지 먼저 확인하는 것이 예약의 첫 단계입니다.</p>",
        f"<p>{move_line}</p>",
        f"<p>{short} 전 지역으로 방문이 가능하며, 자택·숙소·오피스텔·호텔 등 다양한 장소에 대응합니다. "
        f"인접한 {near_txt} 생활권과 경계가 맞닿은 지역은 가까운 쪽 기준으로 안내받는 것이 빠릅니다.</p>",
        "</section>",
    ]

    # 생활권
    life_cards = LIFE_BY_CITY.get(slug, [])
    if life_cards:
        items = [(LIFE_PATH[s], n, "생활권별 방문 가능 지역 안내") for s, n in life_cards]
        body.append(f'<section id="life"><h2>{short} 생활권별 예약 기준</h2>'
                    f"<p>{short}의 주요 생활권을 시·군–읍면동–역세권과 연결해 안내합니다.</p>"
                    + _cards(items) + "</section>")

    # 일반구 또는 대표 동
    if c["gu"]:
        items = [(f"/{slug}/{gslug}/", gname, "구별 대표 동·생활권 안내")
                 for gslug, gname in c["gu"]]
        body.append(f'<section id="gu"><h2>{name} 일반구 안내</h2>'
                    f"<p>{name}는 {len(c['gu'])}개 일반구로 나뉘며, 각 구는 시 전체와 대표 동을 잇는 "
                    "허브 역할을 합니다.</p>" + _cards(items) + "</section>")
    else:
        dong_names = CITY_DONG.get(slug, [])
        if dong_names:
            lis = "".join(f"<li>{dong_link(slug, d)}</li>" for d in dong_names)
            body.append(f'<section id="dong"><h2>{short} 대표 지역 안내</h2>'
                        f"<p>{short}의 대표 동·읍·면 생활권입니다.</p><ul>{lis}</ul></section>")

    # 가까운 역
    if st_names:
        st_items = [(STATION_PATH[STATION_BY_NAME[n]], n, None)
                    for n in st_names if n in STATION_BY_NAME]
        if st_items:
            body.append(f'<section id="stations"><h2>{short} 주요 지하철역 안내</h2>'
                        f"<p>{short}의 대표 역세권별 인접 지역을 확인하세요.</p>"
                        + _cards(st_items) + "</section>")

    # 인접 시·군
    near_links = " · ".join(city_link(n) for n in c["nearby"])
    body.append(f'<section id="nearby"><h2>인접 시·군 안내</h2>'
                f"<p>{short}과 생활권이 맞닿은 인접 시·군입니다: {near_links}. "
                "경계 지역은 가까운 쪽 생활권으로 안내받는 것이 빠릅니다.</p>"
                f'<p><a href="/{grp["slug"]}/">{grp["name"]} 권역 전체 안내</a>에서 '
                "다른 시·군도 함께 확인할 수 있습니다.</p></section>")

    # 확인사항
    body.append(f'<section id="check"><h2>{short} 홈타이 예약 전 확인사항</h2>{CHECK_LIST}</section>')

    body.append(external_refs(slug, c["wiki"]))
    body.append(byline())
    body.append(reservation_note(short))
    body.append(price_table())

    faqs = [
        (f"{short} 전 지역으로 방문이 가능한가요?",
         f"네. {name} 전 지역으로 방문 가능하며, {', '.join(c['life'][:3])} 등 주요 생활권은 "
         "예약 시 가까운 역과 함께 안내해 드립니다."),
        (f"{short}에서 가장 가까운 역을 기준으로 예약해도 되나요?",
         "네. 가까운 역과 생활권을 알려 주시면 방문 주소와 이동 시간을 더 정확히 확인할 수 있습니다."
         + ("" if not st_names else f" {short} 주요 역은 {', '.join(st_names[:4])} 등이 있습니다.")),
        ("추가 이동비는 어떻게 확인하나요?",
         "지역별 기본 이동권이 정해져 있고, 외곽은 추가 이동비가 발생할 수 있습니다. "
         f"예약 전화(<a href=\"tel:{PHONE}\">{PHONE_DISPLAY}</a>) 시 정확히 확인해 드립니다."),
        ("어떤 장소로 방문이 가능한가요?",
         "자택·숙소·오피스텔·호텔 등으로 방문 가능합니다. 건물 출입 방식과 주차 여부를 "
         "미리 알려 주시면 방문이 원활합니다."),
    ]
    body.append(faq_block(faqs, f"{short} 출장마사지 자주 묻는 질문"))

    extra = (image_schema(f"{short} 출장마사지·홈타이 지역 안내",
                          f"{name} 생활권·역세권별 방문 예약 안내")
             + faq_schema(faqs))

    desc = _desc(f"{short} 출장마사지·홈타이 예약 전 {', '.join(c['life'][:4])} 생활권 방문 지역을 확인하세요.")
    title = f"{short} 출장마사지｜{'·'.join(c['life'][:4])} 생활권 안내"
    return {
        "path": f"{slug}/",
        "title": title,
        "desc": desc,
        "h1": f"{name} 출장마사지 · {short} 홈타이 예약 안내",
        "breadcrumb": [("경기도", "/"), (grp["name"], f"/{grp['slug']}/"),
                       (name, "")],
        "body": "\n".join(body),
        "extra_head": extra,
    }


# ========== 일반구 페이지 ==========
def build_gu(city_slug, gu_slug, gu_name):
    c = CITIES[city_slug]
    name, short, group = c["name"], c["short"], c["group"]
    grp = REGION_GROUPS[group]
    dong_names = GU_DONG.get((city_slug, gu_slug), [])

    body = [
        f'<section><h2>{gu_name} 생활권 안내</h2>',
        f"<p>{name} {gu_name}는 {name}를 구성하는 일반구로, 시 전체 안내와 대표 동 생활권을 "
        f"잇는 허브 역할을 합니다. {gu_name} 지역으로 방문 예약 시에는 정확한 동과 가장 가까운 "
        "역을 함께 알려 주시면 이동 시간을 줄일 수 있습니다.</p>",
        f"<p>{gu_name}은 같은 구 안에서도 동마다 상권·주거지·역세권 성격이 달라, 본인 위치가 "
        f"어느 동에 속하는지 먼저 확인하는 것이 좋습니다. 아래 대표 동 안내에서 {gu_name}의 주요 "
        "생활권을 확인하고, 가까운 동·역을 기준으로 예약하시면 방문이 한결 수월합니다. "
        "자택·숙소·오피스텔·호텔 등 다양한 장소로 방문 가능합니다.</p>",
        f'<p><a href="/{city_slug}/">{name} 전체 안내</a>와 함께 보면 생활권을 '
        "더 쉽게 파악할 수 있습니다.</p></section>",
    ]

    if dong_names:
        lis = "".join(f"<li>{dong_link(city_slug, d)} — {gu_name} 생활권</li>" for d in dong_names)
        body.append(f'<section><h2>{gu_name} 대표 동</h2>'
                    f"<p>{gu_name}의 대표 동·생활권입니다.</p><ul>{lis}</ul></section>")

    # 구와 연결되는 역
    gu_stations = []
    for d in dong_names:
        hit = DONG_BY_KEY.get((city_slug, d))
        if hit:
            for dp in DONG_PAGES:
                if dp[0] == hit[0]:
                    gu_stations.extend(dp[4])
    gu_stations = list(dict.fromkeys(gu_stations))
    if gu_stations:
        st_items = [(STATION_PATH[STATION_BY_NAME[n]], n, None)
                    for n in gu_stations if n in STATION_BY_NAME]
        if st_items:
            body.append(f'<section><h2>{gu_name} 인접 역세권</h2>'
                        f"<p>{gu_name} 생활권과 가까운 주요 역입니다.</p>"
                        + _cards(st_items) + "</section>")

    other_gu = [(gs, gn) for gs, gn in c["gu"] if gs != gu_slug]
    if other_gu:
        links = " · ".join(f'<a href="/{city_slug}/{gs}/">{gn}</a>' for gs, gn in other_gu)
        body.append(f'<section><h2>{name} 다른 구 안내</h2><p>{links}</p></section>')

    body.append(f'<section><h2>{gu_name} 예약 전 확인사항</h2>{CHECK_LIST}</section>')
    body.append(byline())
    body.append(reservation_note(f"{short} {gu_name}"))
    body.append(price_table())

    faqs = [
        (f"{gu_name}도 방문 예약이 가능한가요?",
         f"네. {name} {gu_name} 전 지역으로 방문 가능하며, "
         f"{', '.join(dong_names[:3]) if dong_names else short} 생활권을 중심으로 안내합니다."),
        (f"{gu_name}에서 가까운 역은 어디인가요?",
         (f"{', '.join(gu_stations[:4])} 등이 가깝습니다. " if gu_stations else "")
         + "정확한 위치를 알려 주시면 가까운 역 기준으로 안내해 드립니다."),
        ("예약은 어떻게 하나요?",
         f"예약 전화(<a href=\"tel:{PHONE}\">{PHONE_DISPLAY}</a>, 연중무휴 24시간)로 "
         "방문 지역과 시간을 알려 주시면 됩니다."),
    ]
    body.append(faq_block(faqs, f"{gu_name} 자주 묻는 질문"))

    desc = _desc(f"{short} {gu_name} 출장마사지·홈타이 예약 전 "
                 f"{', '.join(dong_names[:3]) if dong_names else short} 생활권을 확인하세요.")
    return {
        "path": f"{city_slug}/{gu_slug}/",
        "title": f"{short} {gu_name} 출장마사지｜대표 동·생활권 안내",
        "desc": desc,
        "h1": f"{name} {gu_name} 출장마사지",
        "breadcrumb": [("경기도", "/"), (grp["name"], f"/{grp['slug']}/"),
                       (name, f"/{city_slug}/"), (gu_name, "")],
        "body": "\n".join(body),
        "extra_head": faq_schema(faqs),
    }


# ========== 읍면동 페이지 ==========
def build_dong(slug, dname, city_slug, gu_slug, near_st, near_dong):
    c = CITIES[city_slug]
    name, short, group = c["name"], c["short"], c["group"]
    grp = REGION_GROUPS[group]
    gu_name = dict(c["gu"]).get(gu_slug) if gu_slug else None
    car = c.get("car", False)

    loc = f"{name} {gu_name} {dname}" if gu_name else f"{name} {dname}"
    st_txt = ", ".join(near_st) if near_st else "차량 이동 기준"

    body = [
        f'<section><h2>{dname} 생활권 안내</h2>',
        f"<p>{loc}은 {short}의 대표 생활권 중 하나로, "
        + (f"가까운 역으로는 {', '.join(near_st)} 등이 있어 방문 접근성이 좋습니다. "
           if near_st else
           "지하철역과 거리가 있어 차량 이동 기준과 추가 이동비를 먼저 확인하는 것이 좋습니다. ")
        + f"{dname} 지역으로 예약하실 때는 정확한 주소와 건물 유형, 가장 가까운 역을 함께 알려 "
        "주시면 이동 시간을 줄일 수 있습니다.</p>",
        f"<p>{dname}으로는 자택·숙소·오피스텔 등 다양한 장소로 방문이 가능하며, "
        f"인접한 {', '.join(near_dong[:3])} 생활권과도 가깝습니다. 예약 전에는 방문 가능 주소와 "
        "예약 가능 시간, 추가 이동비 여부를 확인해 두면 예약이 한결 수월합니다.</p>",
        f"<p>{dname}은 {short} 안에서도 생활권 경계가 비교적 뚜렷한 편이라, 같은 동 안에서도 "
        "아파트 단지·오피스텔·주택가에 따라 가까운 역과 진입로가 달라집니다. 정확한 단지명이나 "
        "건물명을 알려 주시면 가장 빠른 동선으로 안내해 드립니다. "
        + (f"{short}은 외곽 생활권이 넓어 차량 이동 기준과 추가 이동비를 먼저 확인하는 것이 좋습니다."
           if car else
           f"{short}은 도심 생활권이 발달해 가까운 역을 기준으로 방문 시간을 잡으면 편리합니다.")
        + "</p>",
        "</section>",
    ]

    if near_st:
        st_items = [(STATION_PATH[STATION_BY_NAME[n]], n, None)
                    for n in near_st if n in STATION_BY_NAME]
        if st_items:
            body.append(f'<section><h2>{dname} 가까운 역</h2>' + _cards(st_items) + "</section>")
    else:
        body.append(f'<section><h2>{dname} 방문 기준</h2>'
                    f"<p>{dname}은 역세권보다 차량 이동 기준이 중요한 지역입니다. "
                    "차량 진입·주차 가능 여부와 추가 이동비를 예약 시 함께 확인하세요.</p></section>")

    near_dong_links = " · ".join(dong_link(city_slug, d) for d in near_dong)
    body.append(f'<section><h2>인접 지역</h2><p>{dname}과 가까운 인접 지역입니다: '
                f"{near_dong_links}.</p></section>")

    # 상위 링크
    up = f'<a href="/{city_slug}/{gu_slug}/">{gu_name}</a>' if gu_name else city_link(city_slug)
    body.append(f'<section><h2>상위 지역 안내</h2><p>{dname}은 {up} 생활권에 속합니다. '
                f"{city_link(city_slug)} 전체 안내에서 다른 생활권도 확인하세요.</p></section>")

    body.append(place_section(dname))
    body.append(f'<section><h2>{dname} 예약 전 확인사항</h2>{CHECK_LIST}</section>')
    body.append(byline())
    body.append(reservation_note(dname))

    faqs = [
        (f"{dname}도 방문이 가능한가요?",
         f"네. {loc} 전 지역으로 방문 가능합니다. 정확한 주소와 가까운 역을 알려 주시면 "
         "방문 시간을 안내해 드립니다."),
        (f"{dname}에서 가까운 역은 어디인가요?", f"{st_txt} 기준으로 안내해 드립니다."),
        ("예약 전 무엇을 확인하면 되나요?",
         "방문 가능 주소, 예약 가능 시간, 추가 이동비 여부, 건물 출입 방식을 먼저 확인하면 좋습니다."),
    ]
    body.append(faq_block(faqs, f"{dname} 자주 묻는 질문"))

    desc = _desc(f"{dname} 출장마사지·홈타이 예약 전 {st_txt} 인접 생활권과 방문 기준을 확인하세요.")
    crumb = [("경기도", "/"), (grp["name"], f"/{grp['slug']}/"),
             (name, f"/{city_slug}/")]
    if gu_name:
        crumb.append((gu_name, f"/{city_slug}/{gu_slug}/"))
    crumb.append((dname, ""))
    path = f"{city_slug}/{gu_slug}/{slug}/" if gu_slug else f"{city_slug}/{slug}/"
    return {
        "path": path,
        "title": f"{dname} 출장마사지｜{short} {dname} 생활권 안내",
        "desc": desc,
        "h1": f"{dname} 출장마사지",
        "breadcrumb": crumb,
        "body": "\n".join(body),
        "extra_head": faq_schema(faqs),
    }


# ========== 지하철역 페이지 ==========
def build_station(slug, sname, city_slug, lines, areas, nearby_cities):
    c = CITIES[city_slug]
    name, short, group = c["name"], c["short"], c["group"]
    grp = REGION_GROUPS[group]
    line_txt = ", ".join(lines)
    area_links = " · ".join(dong_link(city_slug, a) for a in areas)

    body = [
        f'<section><h2>{sname} 생활권 안내</h2>',
        f"<p>{sname}은 {name}에 위치한 역으로, {line_txt}이(가) 지나갑니다. "
        f"{sname}을 기준으로 한 출장마사지·홈타이 예약은 인접한 {', '.join(areas)} 생활권을 "
        "중심으로 안내합니다. 역명 기준으로 안내하며, 출구별로 페이지를 나누지 않습니다.</p>",
        f"<p>{sname} 인근으로 예약하실 때는 정확한 건물 주소와 출입 방식을 함께 알려 주시면 "
        "방문이 원활합니다. 자택·숙소·오피스텔·호텔 등 다양한 장소로 방문 가능합니다.</p>",
        f"<p>{sname}은 {line_txt} 이용객과 인근 주거지·업무지구 방문 수요가 함께 모이는 곳이라, "
        f"역을 기준으로 {', '.join(areas)} 방향 중 어느 쪽인지 알려 주시면 이동 시간을 더 줄일 수 "
        f"있습니다. {sname} 주변은 시간대에 따라 도로 혼잡도가 달라지므로, 희망 시간대를 미리 "
        "알려 주시면 방문 가능 시간을 정확히 안내해 드립니다.</p>",
        "</section>",
        f'<section><h2>연결 노선</h2><p>{sname}을 지나는 노선은 {line_txt}입니다. '
        "환승역도 역명 기준 한 페이지로 안내하므로 노선별로 따로 찾지 않으셔도 됩니다.</p></section>",
        f'<section><h2>인접 지역</h2><p>{sname}과 가까운 지역입니다: {area_links}.</p></section>',
    ]

    body.append(f'<section><h2>인접 시·군</h2><p>{sname}은 {city_link(city_slug)} 생활권에 속합니다.'
                + (f" 인접한 {', '.join(city_link(n) for n in nearby_cities)} 생활권과도 가깝습니다."
                   if nearby_cities else "")
                + "</p></section>")

    # 관련 생활권
    rel_life = LIFE_BY_CITY.get(city_slug, [])
    if rel_life:
        links = " · ".join(f'<a href="{LIFE_PATH[s]}">{n}</a>' for s, n in rel_life[:3])
        body.append(f'<section><h2>관련 생활권</h2><p>{sname}과 연결되는 생활권: {links}.</p></section>')

    body.append(place_section(sname + " 인근"))
    body.append(f'<section><h2>{sname} 예약 전 확인사항</h2>{CHECK_LIST}</section>')
    body.append(byline())
    body.append(reservation_note(sname))

    faqs = [
        (f"{sname} 근처도 방문이 가능한가요?",
         f"네. {sname} 인근 {', '.join(areas[:2])} 생활권으로 방문 가능합니다. "
         "정확한 주소를 알려 주시면 방문 시간을 안내해 드립니다."),
        (f"{sname}은 어느 노선인가요?", f"{line_txt}이(가) 지나는 역입니다."),
        ("출구별로 예약을 나눠야 하나요?",
         "아니요. 역명 기준으로 안내하므로 출구를 구분하지 않으셔도 됩니다. "
         "정확한 건물 주소만 알려 주시면 됩니다."),
    ]
    body.append(faq_block(faqs, f"{sname} 자주 묻는 질문"))

    desc = _desc(f"{sname} 출장마사지·홈타이 예약 전 {', '.join(areas[:3])} 인접 생활권을 확인하세요.")
    return {
        "path": f"station/{slug}/",
        "title": f"{sname} 출장마사지｜{'·'.join(areas[:2])} 생활권 안내",
        "desc": desc,
        "h1": f"{sname} 출장마사지",
        "breadcrumb": [("경기도", "/"), ("지하철역 안내", "/station/"),
                       (sname, "")],
        "body": "\n".join(body),
        "extra_head": faq_schema(faqs),
    }


# ========== 생활권 페이지 ==========
def build_life(slug, lname, city_slug, areas, stations, role):
    c = CITIES[city_slug]
    name, short, group = c["name"], c["short"], c["group"]
    grp = REGION_GROUPS[group]
    area_links = " · ".join(dong_link(city_slug, a) for a in areas)
    st_links = " · ".join(station_link(s) for s in stations)

    body = [
        f'<section><h2>{lname} 생활권 안내</h2>',
        f"<p>{lname} 생활권은 {city_link(city_slug)} 안의 핵심 권역으로, {role} "
        f"이 생활권은 {', '.join(areas)} 등 지역과 {', '.join(stations) if stations else '차량 이동 중심'} "
        "역을 연결합니다.</p>",
        f"<p>{lname} 생활권으로 출장마사지·홈타이를 예약하실 때는 정확한 동과 가까운 역, "
        "건물 출입 방식을 함께 알려 주시면 방문이 원활합니다. 자택·숙소·오피스텔·호텔 등 "
        "다양한 장소로 방문 가능합니다.</p>",
        f"<p>생활권 페이지는 {short}의 시·군 안내와 읍·면·동, 역세권을 하나로 잇는 허브입니다. "
        f"{lname} 안에서도 단지·건물에 따라 가까운 역과 진입로가 달라지므로, 정확한 위치를 "
        "알려 주시면 같은 생활권 안에서 가장 빠른 동선으로 안내해 드립니다. 인접 생활권과 경계가 "
        "맞닿은 곳은 더 가까운 쪽 기준으로 안내받는 것이 이동 시간을 줄이는 방법입니다.</p>",
        "</section>",
        f'<section><h2>연결 지역</h2><p>{lname} 생활권과 연결되는 지역: {area_links}.</p></section>',
    ]
    if st_links:
        body.append(f'<section><h2>연결 역</h2><p>{lname} 생활권과 연결되는 역: {st_links}.</p></section>')
    body.append(f'<section><h2>관련 시·군</h2><p>{lname} 생활권은 {city_link(city_slug)}에 속하며, '
                f'<a href="/{grp["slug"]}/">{grp["name"]} 권역</a>에서 다른 생활권도 '
                "확인할 수 있습니다.</p></section>")
    body.append(f'<section><h2>{lname} 예약 전 확인사항</h2>{CHECK_LIST}</section>')
    body.append(byline())
    body.append(reservation_note(lname))
    body.append(price_table())

    faqs = [
        (f"{lname} 생활권은 어디를 포함하나요?",
         f"{', '.join(areas)} 등 지역을 포함합니다. 정확한 주소를 알려 주시면 가까운 기준으로 안내합니다."),
        (f"{lname} 생활권에서 가까운 역은 어디인가요?",
         f"{', '.join(stations) if stations else '차량 이동 기준으로 안내드립니다'}."),
        ("예약은 어떻게 하나요?",
         f"예약 전화(<a href=\"tel:{PHONE}\">{PHONE_DISPLAY}</a>)로 생활권과 시간을 알려 주시면 됩니다."),
    ]
    body.append(faq_block(faqs, f"{lname} 생활권 자주 묻는 질문"))

    desc = _desc(f"{lname} 생활권 출장마사지·홈타이 예약 전 {', '.join(areas[:3])} 방문 지역을 확인하세요.")
    return {
        "path": f"life/{slug}/",
        "title": f"{lname} 생활권 출장마사지 안내｜{short}",
        "desc": desc,
        "h1": f"{lname} 생활권 출장마사지 안내",
        "breadcrumb": [("경기도", "/"), ("생활권 안내", "/life/"),
                       (lname, "")],
        "body": "\n".join(body),
        "extra_head": faq_schema(faqs),
    }


# ========== 권역 허브 페이지 ==========
def build_region(group_slug):
    grp = REGION_GROUPS[group_slug]
    cities = grp["cities"]
    items = []
    for cs in cities:
        c = CITIES[cs]
        items.append((f"/{cs}/", c["name"], "·".join(c["life"][:3]) + " 생활권"))

    # 권역 특성 설명 (남/북 구분)
    if group_slug == "south":
        char_p = ("경기남부는 수원·성남·안양·부천처럼 역세권과 도심 생활권이 강한 지역과, "
                  "용인·화성·김포·시흥처럼 신도시 주거 생활권이 빠르게 늘어난 지역, 그리고 "
                  "이천·여주·양평처럼 차량 이동 기준이 중요한 도농복합 지역이 함께 있습니다.")
        big = "수원, 성남, 용인, 화성, 부천, 안산"
    else:
        char_p = ("경기북부는 고양·의정부·구리처럼 도심·신도시 생활권이 발달한 지역과, "
                  "남양주·파주·양주처럼 신도시와 읍·면 생활권이 섞인 지역, 그리고 "
                  "포천·가평·연천처럼 차량 이동과 추가 이동비 확인이 중요한 외곽 지역이 함께 있습니다.")
        big = "고양, 남양주, 파주, 의정부"

    body = [
        f'<section><h2>{grp["name"]} 권역 안내</h2>',
        f"<p>{grp['name']}는 {', '.join(CITY_SHORT[c] for c in cities[:8])} 등 "
        f"{len(cities)}개 시·군으로 이루어진 권역입니다. 이 페이지는 각 시·군 안내로 연결되는 "
        "허브 역할만 하며, 자세한 생활권·역세권 정보는 각 시·군 페이지에서 확인할 수 있습니다.</p>",
        f"<p>{char_p}</p>",
        f"<p>{grp['name']}에서 방문 예약 시에는 본인 위치에서 가장 가까운 시·군을 먼저 선택하고, "
        f"그 안의 생활권과 가까운 역을 기준으로 안내받는 것이 이동 시간을 줄이는 방법입니다. "
        f"{big} 같은 핵심 지역은 생활권 페이지도 함께 제공되어 더 정확한 방문 주소를 확인할 수 "
        "있습니다.</p></section>",
        f'<section><h2>{grp["name"]} 시·군별 안내</h2>'
        f'<p>각 시·군 페이지에서 대표 생활권, 가까운 역, 예약 전 확인사항을 확인하세요.</p>'
        + _cards(items) + "</section>",
    ]
    all_links = " · ".join(city_link(c) for c in cities)
    body.append(f'<section><h2>{grp["name"]} 전체 시·군 바로가기</h2>'
                f"<p>{grp['name']}에 속한 시·군입니다. 본인 위치와 가까운 곳을 선택하세요: "
                f"{all_links}.</p></section>")

    # 권역 내 대표 생활권 링크
    region_life = []
    for cs in cities:
        region_life.extend(LIFE_BY_CITY.get(cs, []))
    if region_life:
        life_links = " · ".join(f'<a href="{LIFE_PATH[s]}">{n}</a>' for s, n in region_life[:12])
        body.append(f'<section><h2>{grp["name"]} 대표 생활권</h2>'
                    f"<p>{grp['name']}의 주요 생활권 페이지에서 시·군·읍면동·역세권을 한 번에 "
                    f"확인할 수 있습니다: {life_links}.</p></section>")
    body.append(f'<section><h2>{grp["name"]} 예약 전 확인사항</h2>{CHECK_LIST}</section>')
    other = "north" if group_slug == "south" else "south"
    body.append(f'<section><h2>다른 권역</h2><p>'
                f'<a href="/{other}/">{REGION_GROUPS[other]["name"]} 안내</a> '
                "및 <a href=\"/\">경기도 전체 안내</a>도 함께 확인하세요.</p></section>")
    body.append(byline())

    desc = _desc(f"{grp['name']} 출장마사지·홈타이 예약 전 "
                 f"{', '.join(CITY_SHORT[c] for c in cities[:5])} 생활권을 확인하세요.")
    return {
        "path": f"{group_slug}/",
        "title": f"{grp['name']} 출장마사지｜{'·'.join(CITY_SHORT[c] for c in cities[:4])} 생활권 안내",
        "desc": desc,
        "h1": f"{grp['name']} 출장마사지 · 권역별 안내",
        "breadcrumb": [("경기도", "/"), (grp["name"], "")],
        "body": "\n".join(body),
    }


# ========== 허브: 지하철역 안내 / 생활권 안내 ==========
def build_station_hub():
    items = [(STATION_PATH[s], n, f"{CITY_SHORT[c]} · {', '.join(a[:2])}")
             for s, n, c, l, a, *_ in STATIONS]
    body = [
        '<section><h2>경기도 주요 지하철역 안내</h2>',
        "<p>경기도 주요 지하철역·광역철도역을 역명 기준으로 안내합니다. 환승역도 역명 기준 한 "
        "페이지로 안내하며, 출구별로 페이지를 나누지 않습니다. 각 역 페이지에서 인접 시·군, "
        "인접 지역, 관련 생활권과 예약 전 확인사항을 확인할 수 있습니다.</p>"
        "<p>본인 위치에서 가장 가까운 역을 선택하면, 인접 생활권과 방문 가능 지역을 함께 "
        "확인할 수 있습니다. 역과 거리가 있는 외곽 지역은 차량 이동 기준과 추가 이동비를 "
        f"<a href=\"/check/\">이용 전 확인사항</a>에서 확인하세요.</p></section>",
        '<section><h2>역명으로 찾기</h2>' + _cards(items) + "</section>",
        '<section><h2>권역·생활권으로 찾기</h2><p>'
        '<a href="/south/">경기남부</a> · <a href="/north/">경기북부</a> 권역과 '
        '<a href="/life/">생활권 안내</a>에서도 지역을 찾을 수 있습니다.</p></section>',
        byline(),
    ]
    return {
        "path": "station/",
        "title": "경기도 지하철역 안내｜역세권별 출장마사지·홈타이 생활권",
        "desc": _desc("경기도 지하철역별 출장마사지·홈타이 인접 생활권과 방문 지역을 확인하세요."),
        "h1": "경기도 지하철역별 안내",
        "breadcrumb": [("경기도", "/"), ("지하철역 안내", "")],
        "body": "\n".join(body),
    }


def build_life_hub():
    items = [(LIFE_PATH[s], n, f"{CITY_SHORT[c]} 생활권")
             for s, n, c, *_ in LIFE_AREAS]
    body = [
        '<section><h2>경기도 생활권별 안내</h2>',
        "<p>생활권 페이지는 시·군, 읍·면·동, 역세권을 하나로 잇는 허브입니다. 같은 시·군 안에서도 "
        "도심 상권, 신도시 주거지, 외곽 생활권의 이동 기준이 다르기 때문에, 생활권 단위로 "
        "확인하면 방문 주소와 이동 시간을 더 정확히 알 수 있습니다.</p>"
        "<p>아래에서 본인 위치와 가까운 생활권을 선택하세요. 각 생활권 페이지에서 연결 지역, "
        "연결 역, 예약 전 확인사항을 확인할 수 있습니다.</p></section>",
        '<section><h2>생활권으로 찾기</h2>' + _cards(items) + "</section>",
        '<section><h2>시·군·역세권으로 찾기</h2><p>'
        '<a href="/">경기도 전체 안내</a>와 '
        '<a href="/station/">지하철역 안내</a>에서도 지역을 찾을 수 있습니다.</p></section>',
        byline(),
    ]
    return {
        "path": "life/",
        "title": "경기도 생활권 안내｜시·군·역세권 연결 출장마사지 안내",
        "desc": _desc("경기도 생활권별 출장마사지·홈타이 연결 지역과 역세권, 방문 기준을 확인하세요."),
        "h1": "경기도 생활권별 안내",
        "breadcrumb": [("경기도", "/"), ("생활권 안내", "")],
        "body": "\n".join(body),
    }


# ========== 전체 조립 ==========
PAGES.append(build_station_hub())
PAGES.append(build_life_hub())
for _gslug in ("south", "north"):
    PAGES.append(build_region(_gslug))

for _slug, _c in CITIES.items():
    PAGES.append(build_city(_slug, _c))
    for _gu_slug, _gu_name in _c["gu"]:
        PAGES.append(build_gu(_slug, _gu_slug, _gu_name))

for _d in DONG_PAGES:
    PAGES.append(build_dong(*_d))

for _s in STATIONS:
    PAGES.append(build_station(*_s))

for _l in LIFE_AREAS:
    PAGES.append(build_life(*_l))
