# 경기도 전지역 출장마사지 사이트 공통 설정

BASE_URL = "https://gyeonggi-massage.pages.dev"

BRAND = "바로 GO"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 운영/저자 정보 (E-E-A-T: 책임 저자·연락처 공개)
EDITOR = "바로 GO 예약상담팀"
EDITOR_ROLE = "경기 전지역 방문 관리 예약 안내"

# 텔레그램 문의 링크 (푸터 오렌지 버튼)
TELEGRAM_BUILD = "https://t.me/googleseolab"   # 웹사이트 제작문의
TELEGRAM_PARTNER = "https://t.me/googleseolab"  # 제휴문의

# 상단 메뉴 — 키워드("출장마사지") 반복 없음. 지역명·역명·생활권명만 노출한다.
NAV = [
    ("경기도 홈", "/gyeonggi/", []),
    ("권역 안내", "/gyeonggi/", [
        ("경기남부", "/gyeonggi/south/"),
        ("경기북부", "/gyeonggi/north/"),
    ]),
    ("시·군 안내", "/gyeonggi/", [
        ("수원시", "/gyeonggi/suwon/"),
        ("성남시", "/gyeonggi/seongnam/"),
        ("용인시", "/gyeonggi/yongin/"),
        ("고양시", "/gyeonggi/goyang/"),
        ("화성시", "/gyeonggi/hwaseong/"),
        ("부천시", "/gyeonggi/bucheon/"),
        ("안산시", "/gyeonggi/ansan/"),
        ("안양시", "/gyeonggi/anyang/"),
        ("남양주시", "/gyeonggi/namyangju/"),
        ("의정부시", "/gyeonggi/uijeongbu/"),
    ]),
    ("지하철역 안내", "/gyeonggi/station/", [
        ("수원역", "/gyeonggi/station/suwon-station/"),
        ("판교역", "/gyeonggi/station/pangyo-station/"),
        ("정자역", "/gyeonggi/station/jeongja-station/"),
        ("기흥역", "/gyeonggi/station/giheung-station/"),
        ("부천역", "/gyeonggi/station/bucheon-station/"),
        ("범계역", "/gyeonggi/station/beomgye-station/"),
        ("의정부역", "/gyeonggi/station/uijeongbu-station/"),
        ("대화역", "/gyeonggi/station/daehwa-station/"),
    ]),
    ("생활권 안내", "/gyeonggi/life/", [
        ("수원역·인계동", "/gyeonggi/life/suwon-station-ingye/"),
        ("분당·판교", "/gyeonggi/life/bundang-pangyo/"),
        ("동탄신도시", "/gyeonggi/life/dongtan-newtown/"),
        ("일산·킨텍스", "/gyeonggi/life/ilsan-kintex/"),
        ("부천역·상동", "/gyeonggi/life/bucheon-station-sangdong/"),
    ]),
    ("예약 안내", "/reservation/", []),
    ("이용 전 확인사항", "/check/", []),
    ("고객센터", "/support/", [
        ("요금 안내", "/pricing/"),
        ("이용 가이드", "/guide/"),
        ("개인정보처리방침", "/support/privacy/"),
    ]),
]
