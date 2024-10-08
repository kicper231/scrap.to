from scrapegraphai.graphs import SmartScraperGraph

from config.settings import PROMPT_PREFIX, PROMPT_SUFFIX


class SmartScraper:

    def __init__(self, api_key, model="openai/gpt-4o-mini"):

        super().__init__()
        self.api_key = api_key
        self.model = model

    def set_model(self, model):
        self.model = model

    def scrap_first_google_search(self, query, prompt, index):
        source = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        prompt = PROMPT_PREFIX + prompt + PROMPT_SUFFIX
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=source,
            config={
                "llm": {
                    "api_key": self.api_key,
                    "model": "openai/" + self.model,
                },
            },
        )

        result = smart_scraper_graph.run()
        return (index, result)

    def scrap_info_from_website(self, url, prompt, index):
        prompt += PROMPT_SUFFIX
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=url,
            config=self.graph_config,
        )
        result = smart_scraper_graph.run()

        return (index, result)
