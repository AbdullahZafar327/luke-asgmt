from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

from scraper import scrape_site
from extractor import extract_structured
from business_map import generate_business_map
from agent_card import generate_agent_card
import asyncio

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class AnalyzeRequest(BaseModel):
    url: str

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    url = req.url.strip()
    if not url.startswith("http"):
        url = "https://" + url
    try:
        # Step 1: Scrape
        pages = await scrape_site(url)
        if not pages:
            raise HTTPException(status_code=400, detail="Could not scrape this URL")

        # Step 2: Deterministic extraction
        extracted = extract_structured(pages)

        # Step 3: LLM Business Map
        biz_map = generate_business_map(extracted)

        # # Step 4: LLM Agent Card (from map only)
        card = generate_agent_card(biz_map, url)

        print(extracted.get("all_discovered_urls", []))

        return {
            "url": url,
            "pages_scraped": extracted["page_count"],
            "all_discovered_urls": extracted.get("all_discovered_urls", []),
            "business_map": biz_map,
            "agent_card": card
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
