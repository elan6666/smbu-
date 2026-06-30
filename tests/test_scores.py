from app.database import query_scores
from app.database import query_dimensions, query_programs


def test_query_scores_filters_province_and_category():
    rows = query_scores(province="广东", category="物理类")
    assert rows
    assert all("广东" in row["province"] for row in rows)
    assert all("物理" in row["category"] for row in rows)


def test_query_scores_missing_returns_empty_list():
    assert query_scores(province="不存在省份") == []


def test_query_programs_finds_undergraduate_degree_mode():
    rows = query_programs(level="本科", degree_mode="双学籍")
    assert any(row["program"] == "经济学" for row in rows)
    assert all("双学籍" in row["degree_mode"] for row in rows)


def test_query_programs_finds_graduate_enrollment():
    rows = query_programs(level="硕士", program="纳米生物技术")
    assert rows
    assert rows[0]["teaching_language"] == "英语"
    assert rows[0]["enrollment_count"] == "15"


def test_query_programs_finds_graduate_category_direction():
    rows = query_programs(level="硕士", program="材料科学与工程")
    assert rows
    assert any(row["program"] == "基础材料学" for row in rows)


def test_query_dimensions_finds_phd_total():
    rows = query_dimensions(level="研究生", keyword="博士")
    assert any(row["value"] == "20" for row in rows)
