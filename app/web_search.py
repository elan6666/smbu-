from __future__ import annotations

import html
from typing import List, Optional
from urllib.parse import parse_qs, unquote, urlparse
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.schemas import SourceSnippet


SEARCH_URL = "https://duckduckgo.com/html/"
OFFICIAL_DOMAINS = ("admission.smbu.edu.cn", "gradadmissions.smbu.edu.cn", "smbu.edu.cn")
OFFICIAL_ENTRYPOINTS = (
    "https://admission.smbu.edu.cn/",
    "https://gradadmissions.smbu.edu.cn/",
    "https://www.smbu.edu.cn/",
)


def _decode_duckduckgo_url(url: str) -> str:
    parsed = urlparse(url)
    if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
        target = parse_qs(parsed.query).get("uddg", [""])[0]
        if target:
            return unquote(target)
    return url


def _is_allowed(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return any(host == domain or host.endswith("." + domain) for domain in OFFICIAL_DOMAINS)


def _clean(text: str) -> str:
    return " ".join(html.unescape(text).split())


def _score_link(query: str, text: str) -> int:
    keywords = [item for item in ["招生", "通知", "最新", "本科", "硕士", "博士", "综合评价", "分数线", "专业"] if item in query]
    return sum(1 for keyword in keywords if keyword in text)


def _search_official_entrypoints(query: str, *, limit: int, timeout: int) -> List[SourceSnippet]:
    candidates = []
    for entrypoint in OFFICIAL_ENTRYPOINTS:
        response = requests.get(
            entrypoint,
            headers={"User-Agent": "SMBUAdmissionAssistant/1.0"},
            timeout=timeout,
        )
        response.raise_for_status()
        response.encoding = response.apparent_encoding or response.encoding
        soup = BeautifulSoup(response.text, "html.parser")
        for anchor in soup.find_all("a"):
            title = _clean(anchor.get_text(" ", strip=True))
            href = anchor.get("href")
            if not title or not href:
                continue
            url = urljoin(entrypoint, href)
            if not _is_allowed(url):
                continue
            score = _score_link(query, title)
            if score <= 0 and "最新" not in query:
                continue
            candidates.append((score, title, url, entrypoint))
    snippets = []
    seen = set()
    for score, title, url, entrypoint in sorted(candidates, key=lambda item: item[0], reverse=True):
        if url in seen:
            continue
        snippets.append(
            SourceSnippet(
                source_id="web_search",
                title=f"联网搜索：{title}",
                url=url,
                snippet=f"来自官方入口 {entrypoint} 的实时链接结果。",
                score=float(score),
            )
        )
        seen.add(url)
        if len(snippets) >= limit:
            break
    return snippets


def search_web(query: str, *, limit: int = 3, timeout: int = 10) -> List[SourceSnippet]:
    scoped_query = (
        f"深圳北理莫斯科大学 {query} "
        "(site:admission.smbu.edu.cn OR site:gradadmissions.smbu.edu.cn OR site:smbu.edu.cn)"
    )
    search_error: Optional[Exception] = None
    try:
        response = requests.get(
            SEARCH_URL,
            params={"q": scoped_query, "kl": "cn-zh"},
            headers={"User-Agent": "SMBUAdmissionAssistant/1.0"},
            timeout=timeout,
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as exc:
        soup = BeautifulSoup("", "html.parser")
        search_error = exc

    snippets: List[SourceSnippet] = []
    seen = set()
    for result in soup.select(".result"):
        link = result.select_one(".result__a")
        if not link:
            continue
        url = _decode_duckduckgo_url(link.get("href", ""))
        if not url or url in seen or not _is_allowed(url):
            continue
        title = _clean(link.get_text(" ", strip=True))
        snippet_node = result.select_one(".result__snippet")
        snippet = _clean(snippet_node.get_text(" ", strip=True)) if snippet_node else title
        snippets.append(
            SourceSnippet(
                source_id="web_search",
                title=f"联网搜索：{title}",
                url=url,
                snippet=snippet[:500],
                score=0.0,
            )
        )
        seen.add(url)
        if len(snippets) >= limit:
            break
    if snippets:
        return snippets

    fallback_results = _search_official_entrypoints(query, limit=limit, timeout=timeout)
    if fallback_results:
        return fallback_results
    if search_error:
        raise search_error
    return snippets


def should_use_web_search(question: str, explicit: bool = False) -> bool:
    if explicit:
        return True
    triggers = ["联网", "网上搜", "搜索", "最新", "现在", "官网现在", "刚发布", "今年新"]
    return any(trigger in question for trigger in triggers)
