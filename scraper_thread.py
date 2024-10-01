from PySide6.QtCore import QThread, Signal

class ScraperThread(QThread):
    result_partial_ready = Signal(dict)
    result_ready = Signal(list)

    def __init__(self, scraper, queries, prompts, urls, mode):
        super().__init__()
        self.scraper = scraper
        self.queries = queries
        self.prompts = prompts
        self.mode = mode
        self.urls = urls

    def run(self):
        results = []
        
        for query, prompt in zip(self.queries, self.prompts):
            result = [] 
            if self.mode == 'Find url' :
             result = self.scraper.scrap_first_google_search(query, prompt)
           
            elif self.mode == 'Url':
             result = self.scraper.scrap_info_from_website(self.urls, prompt)

            self.result_partial_ready.emit(result)    
            results.append(result)

        self.result_ready.emit(results)  