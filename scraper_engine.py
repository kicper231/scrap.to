import os
from scrapegraphai.graphs import SmartScraperGraph, SmartScraperMultiGraph

from PySide6.QtCore import Signal
from PySide6 import QtWidgets, QtCore

class SmartScraper():

    def __init__(self, api_key, model="openai/gpt-4o-mini"):

        super().__init__()
        self.graph_config = {
            "llm": {
                "api_key": api_key,
                "model": model,
            },
        }

    def scrap_first_google_search(self, query, prompt):
        source = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        prompt ="Based on search results: " + prompt + " Please provide the data as flat JSON objects without nesting under any keys or names."
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=source,
            config=self.graph_config,
        )

        result = smart_scraper_graph.run()
        return result

    def scrap_info_from_website(self, urls, prompt):
        
        smart_scraper_graph = SmartScraperMultiGraph(
            prompt=prompt,
            source=urls,
            config=self.graph_config,
        )
        result = smart_scraper_graph.run()
        return result