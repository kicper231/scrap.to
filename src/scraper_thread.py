from concurrent.futures import ThreadPoolExecutor

from PySide6.QtCore import QThread, Signal

from enums import Mode


class ScraperThread(QThread):
    result_partial_ready = Signal(dict)
    result_ready = Signal(list)
    exception_occour = Signal(Exception)

    def __init__(self, scraper, queries, prompts, urls, mode, pararell, chatModel):
        super().__init__()
        self.scraper = scraper
        self.queries = queries
        self.prompts = prompts
        self.mode = mode
        self.urls = urls
        self.pararell = pararell
        self.chatModel = chatModel
        self.stop_flag = False

    def run(self):
        results = []
        self.scraper.set_model(self.chatModel)

        if self.pararell == True:
            with ThreadPoolExecutor() as executor:
                futures = []
                for i in range(len(self.prompts)):

                    if self.stop_flag:
                        break

                    try:
                        if self.mode == Mode.FIND_URL:
                            futures.append(
                                executor.submit(
                                    self.scraper.scrap_first_google_search,
                                    self.queries[i],
                                    self.prompts[i],
                                    i,
                                )
                            )
                        elif self.mode == Mode.URL:
                            futures.append(
                                executor.submit(
                                    self.scraper.scrap_info_from_website,
                                    self.urls[i],
                                    self.prompts[i],
                                    i,
                                )
                            )
                    except Exception as e:
                        self.send_error(e)
                        break

                for future in futures:
                    if self.stop_flag:
                        break

                    try:
                        result = future.result()
                        self.result_partial_ready.emit(result[1])
                        results.append(result)

                    except Exception as e:
                        self.send_error(e)
                        break

            results.sort(key=lambda x: x[0])
            results = [result[1] for result in results]

        elif self.pararell is False:

            for i in range(len(self.prompts)):

                if self.stop_flag:
                    break

                try:
                    if self.mode == Mode.FIND_URL:
                        result = self.scraper.scrap_first_google_search(
                            self.queries[i], self.prompts[i], i
                        )

                    if self.mode == Mode.URL:
                        result = self.scraper.scrap_info_from_website(
                            self.urls[i], self.prompts[i], i
                        )

                    self.result_partial_ready.emit(result[1])
                    results.append(result[1])
                except Exception as e:
                    self.send_error(e)
                    break

        self.result_ready.emit(results)

    def stop(self):
        self._stop_flag = True

    def send_error(self, message):
        self.stop_flag = True
        self.exception_occour.emit(message)
