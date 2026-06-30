from app.router import rule_based_route


def test_rule_based_score_query():
    assert rule_based_route("广东物理类多少分能报") == "score_query"


def test_rule_based_unsupported():
    assert rule_based_route("你能保证我一定录取吗") == "unsupported"


def test_rule_based_major():
    assert rule_based_route("电子与计算机工程专业学什么") == "major_intro"

