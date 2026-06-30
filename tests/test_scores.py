from app.database import query_scores


def test_query_scores_filters_province_and_category():
    rows = query_scores(province="广东", category="物理类")
    assert rows
    assert all("广东" in row["province"] for row in rows)
    assert all("物理" in row["category"] for row in rows)


def test_query_scores_missing_returns_empty_list():
    assert query_scores(province="不存在省份") == []

