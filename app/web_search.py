from __future__ import annotations

import html
from typing import List
from urllib.parse import parse_qs, unquote, urlparse

import requests
from bs4 import BeautifulSoup

from app.schemas import SourceSnippet


SEARCH_URL = "https://duckduckgo.com/html/"
OFFICIAL_DOMAINS = ("admission.smbu.edu.cn", "gradadmissions.smbu.edu.cn", "smbu.edu.cn")


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


def search_web(query: str, *, limit: int = 3, timeout: int = 10) -> List[SourceSnippet]:
    scoped_query = (
        f"深圳北理莫斯科大学 {query} "
        "(site:admission.smbu.edu.cn OR site:gradadmissions.smbu.edu.cn OR site:smbu.edu.cn)"
    )
    response = requests.get(
        SEARCH_URL,
        params={"q": scoped_query, "kl": "cn-zh"},
        headers={"User-Agent": "SMBUAdmissionAssistant/1.0"},
        timeout=timeout,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

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
    return snippets


def should_use_web_search(question: str, explicit: bool = False) -> bool:
    if explicit:
        return True
    triggers = ["联网", "网上搜", "搜索", "最新", "现在", "官网现在", "刚发布", "今年新"]
    return any(trigger in question for trigger in triggers)
