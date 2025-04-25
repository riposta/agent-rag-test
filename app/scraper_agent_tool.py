from agents import Tool
from app.agent_scraper import scrape_domain

scrape_agent_tool = Tool(
    name="scraper",
    description="Pobiera i agreguje wszystkie treści podstron na danej domenie, zaczynając od podanego adresu URL.",
    func=scrape_domain,
)