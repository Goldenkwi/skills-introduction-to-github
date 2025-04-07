# agentql_scraper.py
import agentql
from playwright.sync_api import sync_playwright

def scrape_website(url):
    """Scrape website pake AgentQL."""
    try:
        with sync_playwright() as playwright, playwright.chromium.launch() as browser:
            page = agentql.wrap(browser.new_page())
            page.goto(url)
            page.wait_for_load_state("networkidle")
            print(f"Halaman {url} udah ke-load")
            
            pertanyaan = """
            {
                div(id="bodycontent") {
                    content_div(class="mw-parser-output") {
                        paragraphs[]
                    }
                }
            }
            """

            response = page.query_elements(pertanyaan)
            if response and response.div and response.div.content_div:
                paragraphs = response.div.content_div.paragraphs
                all_paragraph_text = ""
                for paragraph in paragraphs:
                    teks = paragraph.text_content()
                    all_paragraph_text += teks + "\n\n"
                return all_paragraph_text.strip()
            else:
                print(f"Ga ada hasil scrape dari {url}, cek selector AgentQL!")
                return None

    except Exception as e:
        print(f"Error saat scraping {url}: {e}")
        return None

if __name__ == "__main__":
    website_url = "https://id.wikipedia.org/wiki/Joko_Widodo"
    extracted_text = scrape_website(website_url)
    if extracted_text:
        print("\n--- Teks Hasil Scraping ---")
        print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
    else:
        print("Scraping gagal atau tidak ada teks ditemukan.")