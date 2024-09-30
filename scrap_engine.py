import os
from scrapegraphai.graphs import SmartScraperMultiGraph
import time

class SmartScraper:
    def __init__(self, api_key, model="openai/gpt-4o-mini"):
        self.graph_config = {
            "llm": {
                "api_key": api_key,
                "model": model,
            },
        }

    def scrap_first_google_search(self, query, prompt):
        source = [f"https://www.google.com/search?q={query.replace(' ', '+')}"]

        prompt = prompt + "Please provide the data as flat JSON objects without nesting under any keys or names."
        print(prompt)
        smart_scraper_graph = SmartScraperMultiGraph(
            prompt=prompt,
            source=source,
            config=self.graph_config,
        )
        result = smart_scraper_graph.run()
        print(result)
        return result

    def scrap_info_from_website(self, prompt, urls):
        
        smart_scraper_graph = SmartScraperMultiGraph(
            prompt=prompt,
            source=urls,
            config=self.graph_config,
        )
        result = smart_scraper_graph.run()
        return result

    def parse_results(self, results):
         pass