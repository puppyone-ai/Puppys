import requests, lxml
from bs4 import BeautifulSoup

headers = {
  "User-agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
  "q": "32*3/3+12*332-1991",
}

def get_calculator_answerbox():
  html = requests.get('https://www.google.com/search', headers=headers, params=params)
  soup = BeautifulSoup(html.text, 'lxml')

  print(soup)

  math_expression = soup.select_one('.XH1CIc').text.strip().replace(' =', '')
  calc_answer = soup.select_one('#cwos').text.strip()
  
  print(f"Expression: {math_expression}\nAnswer: {calc_answer}")


get_calculator_answerbox()