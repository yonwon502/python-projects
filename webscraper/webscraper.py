import requests
from bs4 import BeautifulSoup
import json

def fetch_page(url):
    """Fetch the page with professional browser headers to bypass basic bot systems."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    print("\n[INFO] Connecting to the website securely...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[ERROR] Failed to fetch the website. Error: {e}")
        return None

def analyze_html(html_content):
    """Professionally analyze HTML to extract eCommerce and Article data."""
    soup = BeautifulSoup(html_content, "html.parser")
    results = {
        "title": None,
        "description": None,
        "products": [],
        "main_content": []
    }

    # 1. Extract Page Title
    if soup.title and soup.title.string:
        results["title"] = soup.title.string.strip()

    # 2. Extract SEO Metadata (super useful for e-commerce and articles)
    og_title = soup.find("meta", property="og:title")
    og_desc = soup.find("meta", property="og:description")
    meta_desc = soup.find("meta", attrs={"name": "description"})

    if og_title and og_title.get("content"):
        results["title"] = og_title["content"].strip()
    if og_desc and og_desc.get("content"):
        results["description"] = og_desc["content"].strip()
    elif meta_desc and meta_desc.get("content"):
        results["description"] = meta_desc["content"].strip()

    # 3. Extract JSON-LD (Rich Data Schema used by eCommerce sites for products)
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            # Some scripts might contain bad formatting, but we'll try to parse it
            data = json.loads(script.string if script.string else "{}")
            # JSON-LD can be a list or a single object
            items = data if isinstance(data, list) else [data]
            for item in items:
                # Sometimes there's a graph structure
                if "@graph" in item:
                    sub_items = item["@graph"]
                else:
                    sub_items = [item]
                
                for sub in sub_items:
                    item_type = sub.get("@type", "")
                    if item_type in ["Product", "Article", "NewsArticle"]:
                        name = sub.get("name") or sub.get("headline") or "Unknown Name"
                        desc = sub.get("description", "")
                        results["products"].append(f"[{item_type}] {name} - {desc[:100]}...")
        except:
            pass # ignore JSON parse errors

    # 4. Extract Main Content (Headings and meaningful text blocks)
    # We remove scripts and styles so they don't pollute the text extraction
    for bad_tag in soup(["script", "style", "nav", "footer", "header"]):
        bad_tag.extract()

    seen_texts = set()
    for tag in soup.find_all(["h1", "h2", "h3", "p", "span", "li", "a", "div"]):
        # Get raw text string
        text = tag.get_text(separator=" ", strip=True)
        # Keep text that looks like a meaningful sentence or product title (>40 chars)
        if text and 40 < len(text) < 500 and text not in seen_texts:
            seen_texts.add(text)
            results["main_content"].append(text)

    # Check if the page is likely a Captcha challenge (Amazon, Cloudflare, etc.)
    if "robot check" in (results["title"] or "").lower() or "captcha" in html_content.lower() or "verify you are human" in html_content.lower():
        results["bot_blocked"] = True

    return results

def main():
    print("=============================================================")
    print("[RUN] Pro Web Scraper (Articles, eCommerce, Metadata Analyzer)")
    print("=============================================================")

    url = input("Enter a website URL: ").strip()

    if not url:
        print("Please enter a valid URL.")
        return

    if not url.startswith("http"):
        url = "https://" + url

    html = fetch_page(url)
    if not html:
        return

    data = analyze_html(html)

    print("\n--- [PAGE SUMMARY] ---")
    print(f"Title: {data['title'] or 'No Title Found'}")
    if data['description']:
        print(f"Description: {data['description']}")

    if data.get("bot_blocked"):
        print("\n[WARN] WARNING: The website restricted access by returning a CAPTCHA or Bot check.")
        print("   Giant eCommerce sites like Amazon heavily block simple scripts. To scrape them,")
        print("   you would need tools like Selenium/Playwright or a paid proxy API.")
        return

    if data["products"]:
        print("\n--- [STRUCTURED DATA] (Products / Articles Found) ---")
        for p in data["products"]:
            print(f"- {p}")

    print("\n--- [HIGHLIGHTED CONTENT] (Snippets) ---")
    # Only show top 15 results so we don't flood the terminal
    highlights = data["main_content"][:15]
    if highlights:
        for idx, text in enumerate(highlights, 1):
            if len(text) > 120:
                text = text[:117] + "..."
            print(f"{idx}. {text}")
    else:
        print("No significant text blocks found.")

if __name__ == "__main__":
    main()