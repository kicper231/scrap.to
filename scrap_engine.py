import os
from scrapegraphai.graphs import SmartScraperMultiGraph
import time

graph_config = {
    "llm": {
        "api_key": "yourKey",
        "model": "openai/gpt-4o-mini",
    },
}

class PersonInfo:
    def __init__(self, name, company, role):
        self.name = name  
        self.company = company  
        self.role = role
       

    def introduce(self):
        print(f"Cześć! Mam na imię {self.name}, pracuję w {self.company} jako {self.role}.")

def get_linkedin_profile(company):
    # Construct the search query
   # query = f"{person.name} {person.company} {person.role} LinkedIn"
    query = f"{company}"
    query
    # Create the SmartScraperGraph instance
    smart_scraper_graph = SmartScraperMultiGraph(
        # prompt=f"Znajdź pierwszy link do profilu LinkedIn dla osoby o następujących danych: {person.name}, {person.company}, {person.role}. Zwróć tylko URL.",
        prompt=f"Znajdz firmę która zajmuję się tematem badan klinicznych, zwroc pierwszy link z wyszukiwań  Nazwa firmy: {company} Oceń czy ta firma to site - przerowadza badania, software - towrzy software czy coś jeszcze innego. Zwróć tylko URL i ocene",
      #  source=[f"https://www.google.com/search?q={query.replace(' ', '+')}"],
        source =[],
        config=graph_config
    )

    # Run the scraper
    result = smart_scraper_graph.run()
    return result

def get_linkedin_profiles(person_list):
    linkedin_links = []
    for person in person_list:
        link = get_linkedin_profile(person)
        linkedin_links.append(link)
        print(link)
    return linkedin_links


   


    
    # print('------------------------start-------------------')

    # # Get the LinkedIn profile link
    # linkedin_profile_links = get_linkedin_profiles(company)
    # print("\nLista profili LinkedIn:")
    # for link in linkedin_profile_links:
    #     print(link)