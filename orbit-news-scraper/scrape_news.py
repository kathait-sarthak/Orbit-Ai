import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news" # You can change this URL to another news website

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    print(f"Attempting to fetch news from: {URL}")
    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status() # Raise an exception for HTTP errors

    soup = BeautifulSoup(response.content, 'html.parser')

    # This selector might need adjustment based on the actual website's HTML structure.
    # Common headline tags for news sites are h2, h3, or h4 within specific divs.
    # For BBC News, h3 tags within specific classes are often used for article titles.
    headlines = soup.find_all(['h2', 'h3']) # Try both h2 and h3 for broader coverage

    found_headlines = []
    seen_texts = set() # To avoid duplicate headlines

    for headline in headlines:
        text = headline.get_text(strip=True)
        # Filter out short or non-meaningful text that might be captured by generic tags
        if text and len(text) > 10 and text not in seen_texts:
            found_headlines.append(text)
            seen_texts.add(text)
        if len(found_headlines) >= 5:
            break

    if found_headlines:
        with open("news.txt", "w", encoding="utf-8") as f:
            for i, headline_text in enumerate(found_headlines):
                f.write(f"{i+1}. {headline_text}\n")
        print("Successfully scraped and saved top news headlines to news.txt")
    else:
        print("No significant headlines found on the page or could not parse the content effectively.")

except requests.exceptions.Timeout:
    print(f"Error: The request to {URL} timed out after 10 seconds.")
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL {URL}: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
