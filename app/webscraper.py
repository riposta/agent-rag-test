import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def scrape_domain(start_url, max_pages=50):
    visited = set()
    results = []

    domain = urlparse(start_url).netloc

    def scrape(url):
        if url in visited or len(visited) >= max_pages:
            return
        try:
            response = requests.get(url, timeout=10)
            if not response.ok:
                return
        except Exception:
            return
        visited.add(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text(separator=' ', strip=True)
        results.append({"url": url, "text": page_text})

        for link in soup.find_all('a', href=True):
            abs_url = urljoin(url, link['href'])
            # Ignore mailto, javascript etc.
            if not abs_url.startswith('http' or 'https'):
                continue
            if urlparse(abs_url).netloc != domain:
                continue  # Only stay in starting domain
            scrape(abs_url)

    scrape(start_url)
    return results
