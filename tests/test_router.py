from app.router import rule_based_route


def test_rule_based_score_query():
    assert rule_based_route("广东物理类多少分能报") == "score_query"


def test_rule_based_unsupported():
    assert rule_based_route("你能保证我一定录取吗") == "unsupported"


def test_rule_based_major():
    assert rule_based_route("电子与计算机工程专业学什么") == "major_intro"


def test_rule_based_greeting_and_clarification():
    assert rule_based_route("你好") == "greeting"
    assert rule_based_route("啥意思") == "clarification"


def test_rule_based_daily_chat():
    assert rule_based_route("你是谁") == "daily_chat"
    assert rule_based_route("谢谢你") == "daily_chat"
