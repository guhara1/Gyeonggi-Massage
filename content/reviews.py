# 리뷰·평점 스키마 데이터 (Service.aggregateRating / review)
#
# ⚠️ 중요: 구글·네이버는 "실제 고객 후기"가 아닌 자작 리뷰/평점을 정책 위반으로 보고
#    리치결과 제외·수동 패널티를 줄 수 있습니다. 반드시 실제 후기만 넣으세요.
#
# 사용법:
#   1) 아래 REVIEWS 에 실제 후기를 채운다.
#   2) ENABLE_REVIEWS = True 로 바꾼다.
#   3) python3 build.py 다시 실행.
#   그러면 모든 지역 페이지의 Service 스키마에 aggregateRating + review 가 들어간다.

ENABLE_REVIEWS = False

# 실제 후기만! (author=실명/닉네임, rating=1~5, date=YYYY-MM-DD, body=후기 본문)
# 예시 형식:
#   ("김**", 5, "2026-05-12", "예약부터 방문까지 정확했고 관리도 만족스러웠습니다."),
REVIEWS = [
    # ("닉네임", 5, "2026-05-12", "실제 후기 내용"),
]


def aggregate():
    """REVIEWS 로부터 평균 평점·개수 계산. 리뷰 없으면 None."""
    if not (ENABLE_REVIEWS and REVIEWS):
        return None
    vals = [r[1] for r in REVIEWS]
    avg = round(sum(vals) / len(vals), 1)
    return {"ratingValue": avg, "reviewCount": len(REVIEWS),
            "bestRating": 5, "worstRating": 1}


def review_schema_list():
    """Review 객체 리스트 (Service.review 용)."""
    if not (ENABLE_REVIEWS and REVIEWS):
        return []
    out = []
    for author, rating, date, body in REVIEWS:
        out.append({
            "@type": "Review",
            "author": {"@type": "Person", "name": author},
            "datePublished": date,
            "reviewRating": {"@type": "Rating", "ratingValue": rating,
                             "bestRating": 5, "worstRating": 1},
            "reviewBody": body,
        })
    return out
