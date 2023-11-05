from serpapi import GoogleSearch

params = {
  "q": "Coffee",
  "location": "Austin, Texas, United States",
  "hl": "en",
  "gl": "us",
  "google_domain": "google.com",
  "api_key": "secret_api_key"
}

search = GoogleSearch(params)
results = search.get_dict()