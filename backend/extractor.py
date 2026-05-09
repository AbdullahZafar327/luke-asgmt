from bs4 import BeautifulSoup
import re

def extract_structured(pages: dict) -> dict:
    all_text = ""
    forms = []
    links = []
    contact = {}
    third_party = []

    all_urls = set()
    for page in pages.values():
        for u in page.get("all_discovered_urls", []):
            all_urls.add(u)

    for url, page in pages.items():
        html = page.get("html", "")
        soup = BeautifulSoup(html, "lxml")
        all_text += page.get("text", "") + "\n"

        # forms
        for f in soup.find_all("form"):
            action = f.get("action", "")
            inputs = [i.get("name","") for i in f.find_all("input")]
            forms.append({"page": url, "action": action, "fields": inputs})

        # links
        for a in soup.find_all("a", href=True):
            links.append({"text": a.get_text(strip=True), "href": a["href"]})

        # contact info
        phones = re.findall(r'\+?[\d\s\-\(\)]{7,15}', all_text)
        emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', all_text)
        if phones: contact["phone"] = phones[0]
        if emails: contact["email"] = emails[0]

        # third-party widgets
        for script in soup.find_all("script", src=True):
            src = script["src"]
            for svc in ["calendly","opentable","shopify","stripe","square","booking.com","paypal"]:
                if svc in src.lower():
                    third_party.append(svc)

    return {
        "pages_found": list(pages.keys()),
        "page_count": len(pages),
        "all_discovered_urls": sorted(all_urls),
        "forms": forms[:5],
        "sample_links": links[:20],
        "contact": contact,
        "third_party_tools": list(set(third_party)),
        "raw_text_sample": all_text[:3000]
    }
