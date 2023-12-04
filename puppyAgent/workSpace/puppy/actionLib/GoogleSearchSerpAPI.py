from serpapi import GoogleSearch
import json
import openai

## Search for the top results

class GoogleSearchSerpy():
    def __init__(self,searchContent, apiKey,location="China",pickingNum=3):
        self.discription="This is a google search function, it can search for information via GoogleSearch, it's aviliable anytime you search"
        self.search_content = searchContent
        self.location=location
        self.pickingNum=pickingNum
        self.apiKey=apiKey

    def setDiscription(self,discription):
        self.discription=discription

    def setAPIKey(self,apiKey):
        self.apiKey=apiKey

    def run(self):

        params = {
        "q": self.search_content,
        "location": self.location,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": self.apiKey,
        }

        search = GoogleSearch(params)
        results = search.get_dict()


        ## pickup the answer box
        if "answer_box" in results:
            answer_box_results={}



            if results["answer_box"]["type"]=="calculator_result":
                answer_box_results={
                    "type":"calculator_result",
                    "answer":results["answer_box"]["answer"],
                }

            elif results["answer_box"]["type"]=="weather_result":
                answer_box_results={
                    "type":"weather_result",
                    "answer":results["answer_box"]["temperature"],
                    "unit":results["answer_box"]["unit"],
                    "weather":results["answer_box"]["weather"],
                    "precipitation":results["answer_box"]["precipitation"],
                    "humidity":results["answer_box"]["humidity"],
                    "wind":results["answer_box"]["wind"],
                }
            
            # if result is in the type of finance_results
            elif results["answer_box"]["type"] == "finance_results":
                answer_box_results = {
                    "type": "finance_results",
                    "title": results["answer_box"]["title"],
                    "exchange": results["answer_box"]["exchange"],
                    "stock": results["answer_box"]["stock"],
                    "currency": results["answer_box"]["currency"],
                    "price": results["answer_box"]["price"],
                    "price_movement": results["answer_box"]["price_movement"],
                    "market": results["answer_box"]["market"],
                    "previous_close": results["answer_box"]["previous_close"],
                    "table": results["answer_box"]["table"],
                }

            # if result is the population result
            elif results["answer_box"]["type"] == "population_result":
                answer_box_results = {
                    "type": "population_result",
                    "place": results["answer_box"]["place"],
                    "population": results["answer_box"]["population"],
                    "year": results["answer_box"]["year"],
                    "sources": results["answer_box"]["sources"]
                }

            # if result is the currency converter
            elif results["answer_box"]["type"] == "currency_converter":
                answer_box_results = {
                    "type": "currency_converter",
                    "result": results["answer_box"]["result"],
                    "price": results["answer_box"]["price"],
                    "currency": results["answer_box"]["currency"],
                    "date": results["answer_box"]["date"],
                    "currency_converter_details": results["answer_box"]["currency_converter"],
                    "chart": results["answer_box"]["chart"]
                }

            # if the result is about the flight
            elif results["answer_box"]["type"] == "google_flights":
                answer_box_results = {
                    "type": "google_flights",
                    "title": results["answer_box"]["title"],
                    "flights": results["answer_box"]["flights"],
                    "search_information": results["answer_box"]["search_information"],
                }

            # if the result is about the flight duration
            elif results["answer_box"]["type"] == "flight_duration":
                answer_box_results = {
                    "type": "flight_duration",
                    "duration": results["answer_box"]["duration"],
                    "stops": results["answer_box"]["stops"],
                    "direction": results["answer_box"]["direction"]
                }

            # if the result is about the hotels
            elif results["answer_box"]["type"] == "hotels":
                answer_box_results = {
                    "type": "hotels",
                    "query": results["answer_box"]["query"],
                    "hotels": results["answer_box"]["hotels"],
                    "map_results": results["answer_box"]["map_results"]
                }

            # if the result is a dictionary result
            elif results["answer_box"]["type"] == "dictionary_results":
                answer_box_results = {
                    "type": "dictionary_results",
                    "syllables": results["answer_box"]["syllables"],
                    "pronunciation_audio": results["answer_box"]["pronunciation_audio"],
                    "phonetic": results["answer_box"]["phonetic"],
                    "word_type": results["answer_box"]["word_type"],
                    "definitions": results["answer_box"]["definitions"],
                    "examples": results["answer_box"]["examples"],
                    "extras": results["answer_box"]["extras"]
                }

            # if result is in the type of organic_result
            elif results["answer_box"]["type"] == "organic_result":
                answer_box_results = results["answer_box"]["organic_result"]

            # if result is in the type of translation_result
            elif results["answer_box"]["type"] == "translation_result":
                answer_box_results = {
                    "type": "translation_result",
                    "source": {
                        "language": results["answer_box"]["translation"]["source"]["language"],
                        "text": results["answer_box"]["translation"]["source"]["text"],
                        "pronunciation": results["answer_box"]["translation"]["source"]["pronunciation"]
                    },
                    "target": {
                        "language": results["answer_box"]["translation"]["target"]["language"],
                        "text": results["answer_box"]["translation"]["target"]["text"]
                    },
                    "interjections": results["answer_box"]["translation"]["interjection"]
                }

            # if the result is directions
            elif results["answer_box"]["type"] == "directions":
                answer_box_results = {
                    "type": "directions",
                    "from": results["answer_box"]["from"],
                    "to": results["answer_box"]["to"],
                    "routes": [{
                        "summary": route["summary"],
                        "formatted": {
                            "duration": route["formatted"]["duration"],
                            "distance": route["formatted"]["distance"],
                            "via": route["formatted"]["via"]
                        },
                    } for route in results["answer_box"]["routes"]]
                }

            # if the result is about the formula
            elif results["answer_box"]["type"] == "formula":
                answer_box_results = {
                    "type": "formula",
                    "title": results["answer_box"]["title"],
                    "solve_for": results["answer_box"]["solve_for"],
                    "solve_for_alternatives": results["answer_box"]["solve_for_alternatives"],
                    "answer": results["answer_box"]["answer"],
                    "answer_alternatives": results["answer_box"]["answer_alternatives"],
                    "parameters": [{
                        "symbol": parameter["symbol"],
                        "name": parameter["name"],
                        "value": parameter["value"],
                        "unit": parameter["unit"]
                    } for parameter in results["answer_box"]["parameters"]],
                    "solutions": results["answer_box"]["solutions"]
                }

            # if the result is about the unit converter
            elif results["answer_box"]["type"] == "unit_converter":
                answer_box_results = {
                    "type": "unit_converter",
                    "unit_type": results["answer_box"]["unit_type"],
                    "from": {
                        "value": results["answer_box"]["from"]["value"],
                        "unit": results["answer_box"]["from"]["unit"]
                    },
                    "to": {
                        "value": results["answer_box"]["to"]["value"],
                        "unit": results["answer_box"]["to"]["unit"]
                    },
                    "formula": results["answer_box"]["formula"]
                }

            # if the result is about the time
            elif results["answer_box"]["type"] == "time":
                answer_box_results = {
                    "type": "time",
                    "result": results["answer_box"]["result"],
                    "date": results["answer_box"]["date"],
                    "description": results["answer_box"]["description"]
                }

            # 假设 `results` 是一个包含解析后的JSON数据的字典
            elif results["answer_box"]["type"] == "air_quality":
                answer_box_results = {
                    "type": "air_quality",
                    "sources": results["answer_box"]["sources"],
                    "full_stations_table": results["answer_box"]["full_stations_table"]
                }

            # 假设 `results` 是一个包含解析后的JSON数据的字典
            elif results["answer_box"]["type"] == "hours":
                answer_box_results = {
                    "type": "hours",
                    "result": results["answer_box"]["result"],
                    "description": results["answer_box"]["description"],
                }

        else:
            answer_box=[]

        if "organic_results" in results:
            organic_results=results["organic_results"]

            ## pick the top3 results for the organic results
            organic_results_brief=[]


            for element in organic_results:
                organic_results_brief_element=[]
                if element["position"]<=self.pickingNum:
                    organic_results_brief_element={
                        "position":
                        element["position"],
                        "title":
                        element["title"],
                        "source":
                        element["source"],
                        "snippet":
                        element["snippet"],
                    }
                
                    organic_results_brief.append(organic_results_brief_element)
            
                else:
                    pass

        else:
            organic_results_brief=[]

        final_answer={
            "answer_box":
            answer_box_results,
            "organic_results":
            organic_results_brief,
        }

        return final_answer



if __name__ == '__main__':
    text="Rockefeller Center hours"
    location="Austin,Texas,United States"
    apiKey="72b0b910c9b0c16277b7295ff1e271b945610f0e4dcec66359d9a91b344a56e1"
    pickingNum=3
    GoogleSearch=GoogleSearchSerpy(text,apiKey,location,pickingNum)
    result=GoogleSearch.run()
    print(result)
