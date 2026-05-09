import asyncio
from crawl4ai import AsyncWebCrawler
from urllib.parse import urljoin, urlparse

async def scrape_site(url: str, max_pages: int = 2) -> dict:
    pages = {}
    to_visit = {url}
    visited = set()
    all_discovered_urls = set() 
    base = urlparse(url).netloc

    async with AsyncWebCrawler(verbose=False) as crawler:
        while to_visit and len(visited) < max_pages:
            current = to_visit.pop()
            if current in visited:
                continue
            try:
                result = await crawler.arun(url=current)

                # collect ALL internal links discovered on this page
                for link in result.links.get("internal", []):
                    href = link.get("href", "")
                    full = urljoin(url, href)
                    if urlparse(full).netloc and href.startswith("http"):
                        all_discovered_urls.add(full)

                pages[current] = {
                    "url": current,
                    "text": result.markdown[:4000],
                    "html": result.html[:8000],
                    "links": result.links.get("internal", [])
                }
                visited.add(current)

                for link in result.links.get("internal", [])[:5]:
                    href = link.get("href", "")
                    full = urljoin(url, href)
                    if urlparse(full).netloc == base and full not in visited:
                        to_visit.add(full)

            except Exception as e:
                pages[current] = {"url": current, "error": str(e)}
                visited.add(current)


    for page in pages.values():
        page["all_discovered_urls"] = sorted(all_discovered_urls)

    return pages