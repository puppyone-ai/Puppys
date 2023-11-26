import requests, lxml
from bs4 import BeautifulSoup

headers = {
  "User-agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

test_queries = [
  'skyscanner customer service phone number',
  'ryanair phone number uk',
  'wizz air phone number',
  'apple online customer service phone number',
  'amazon phone number',
  'walmart online phone number',
  'imb bank online phone number',
  'target online phone number',
  'yelp online phone number'
]

def get_phone_answer_box():

  for query in test_queries:
    params = {
      "q": query,
      "hl": "en",
      "gl": "us"
    }
    
    html = requests.get('https://www.google.com/search', headers=headers, params=params)
    soup = BeautifulSoup(html.text, 'lxml')

    print(soup)
  
    # several CSS selectors to cover multiple layouts
    phone_number = soup.select_one('.d9FyLd b, .IZ6rdc, .EfDVh, .mw31Ze, .hgKElc b').text
    print(phone_number)

get_phone_answer_box()