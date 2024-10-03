from PySide6.QtCore import QThread, Signal
from mode_enum import Mode
from concurrent.futures import ThreadPoolExecutor

class ScraperThread(QThread):
    result_partial_ready = Signal(dict)
    result_ready = Signal(list)

    def __init__(self, scraper, queries, prompts, urls, mode, pararell):
        super().__init__()
        self.scraper = scraper
        self.queries = queries
        self.prompts = prompts
        self.mode = mode
        self.urls = urls
        self.pararell = pararell

    def run(self):
        results = []
        if self.pararell == True:
            with ThreadPoolExecutor() as executor:
                futures = []
                for i in range(len(self.prompts)):
                    if self.mode == Mode.FIND_URL:
                        futures.append(executor.submit(self.scraper.scrap_first_google_search, self.queries[i], self.prompts[i]))
                    elif self.mode == Mode.URL:
                        futures.append(executor.submit(self.scraper.scrap_info_from_website, self.urls[i], self.prompts[i]))

                for future in futures:
                    result = future.result()
                    self.result_partial_ready.emit(result)
                    results.append(result)                 

        elif self.pararell == False:

            for i in range(len(self.prompts)):

             if self.mode == Mode.FIND_URL:
              result = self.scraper.scrap_first_google_search(self.queries[i], self.prompts[i])

             if self.mode == Mode.URL:
               result = self.scraper.scrap_info_from_website(self.urls[i], self.prompts[i])

             self.result_partial_ready.emit(result)    
             results.append(result)
        
        self.result_ready.emit(results)
     
