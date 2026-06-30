from app.rag import search


def test_search_returns_fallback_or_indexed_sources():
    results = search("招生章程 录取规则", limit=3)
    assert results
    assert results[0].title
    assert results[0].url

