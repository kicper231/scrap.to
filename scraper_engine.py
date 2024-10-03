import os
from scrapegraphai.graphs import SmartScraperGraph, SmartScraperMultiGraph

from PySide6.QtCore import Signal
from PySide6 import QtWidgets, QtCore

class SmartScraper():

    sufix = " Please provide the data as flat JSON objects without nesting under any keys or names."

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
        print(source)

        prompt ="Based on search results: " + prompt + self.sufix
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=source,
            config=self.graph_config,
        )

        result = smart_scraper_graph.run()
        return result

    def scrap_info_from_website(self, url, prompt):
        prompt+=self.sufix
        print(url)
        smart_scraper_graph = SmartScraperGraph(
            prompt= prompt,
            source = url,
            config=self.graph_config,
        )
        result = smart_scraper_graph.run()
    
        return result