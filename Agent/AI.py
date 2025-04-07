# ai.py
import sys
import google.generativeai as genai
from agentql_scraper import scrape_website
from search import Search

# Setup Gemini API
genai.configure(api_key="AIzaSyD11-l9-HYew5QvfrKN7ElS06NSuNQM0zE")
model = genai.GenerativeModel("models/gemini-1.5-flash")

conversation_history = []
search_engine = Search()

def summarize_webpages(urls):
    """Scrape dan summarize konten dari beberapa website pake Gemini."""
    combined_text = ""
    for url in urls:
        print(f"Scraping website: {url}...")
        website_text = scrape_website(url)
        if website_text:
            combined_text += website_text + "\n\n"
        else:
            print(f"Gagal scrape: {url}.")
            return None

    if not combined_text:
        return "Gak ada teks yang di-scrape bro."

    summary_prompt = f"""
    Buat ringkasan padat dan informatif dari teks berikut:
    --- TEKS WEBSITE ---
    {combined_text}
    --- END TEKS WEBSITE ---
    RINGKASAN:
    """

    try:
        response = model.generate_content(summary_prompt)
        if response and response.text:
            return response.text.strip()
        else:
            print("Gak ada respons dari Gemini.")
            return "Gagal dapetin ringkasan dari Gemini."
    except Exception as e:
        print(f"Error bro: {e}")
        return f"Error saat minta ringkasan: {e}"

# Fungsi buat chat biasa
def generate_response(prompt, history):
    full_prompt = "\n".join([msg["content"] for msg in history]) + "\n" + prompt
    try:
        response = model.generate_content(full_prompt)
        if response and response.text:
            return response.text.strip()
        else:
            return "Gak ada respons dari Gemini."
    except Exception as e:
        return f"Error bro: {e}"

# Inisiasi history
conversation_history.append({"role": "system", "content": "Filsuf nihilis absurdisme, netral dan intelektual."})

# Main loop
while True:
    ngobrol = search_engine.get_user_query()

    if ngobrol.lower().startswith("search "):
        query = ngobrol[7:]
        print(f"Nyanyi '{query}' di Google...")
        links = search_engine.google_search(query)
        if links:
            summary = summarize_webpages(links[:3])
            if summary:
                print("\n> Assistant (Summary):")
                print(summary)
            else:
                print("> Assistant: Gagal scrape atau summarize bro.")
        else:
            print("> Assistant: Gak ada link ditemuin.")

    elif ngobrol.lower().startswith("summarize website"):
        urls = [part for part in ngobrol.split() if part.startswith("http")]
        if urls:
            print("Summarizing bro...")
            summary = summarize_webpages(urls)
            if summary:
                print("\n> Assistant (Summary):")
                print(summary)
            else:
                print("> Assistant: Gagal summarize bro.")
        else:
            print("> Assistant: Kasih URL bro, contoh: 'summarize website https://example.com'")

    else:
        conversation_history.append({"role": "user", "content": ngobrol})
        reply = generate_response(ngobrol, conversation_history)
        print("\n> Assistant:")
        print(reply)
        conversation_history.append({"role": "assistant", "content": reply})