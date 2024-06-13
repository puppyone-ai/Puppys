# If you are a VS Code users:
#import sys
#import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy.actions import check, do, score
from puppy import light, Puppy

# change the API key to your own
#os.environ["OPENAI_API_KEY"] = ""
Mei = Puppy(name="Mei")

url = "https://news.ycombinator.com/"

Mei.test()

@light
def hacker_news():

    html = Mei.do(f"go to {url} show the HTML")

    news = Mei.do(f"extract the news from the {html}")

    for stuff in news:
        related_score = score(f'how {stuff} is related to Large Language Models)')
        if check(f'{related_score} is higher than 5'):  # if related_score>5:
            Mei.do(f"summarize the {stuff}, and send it to me")


if __name__ == "__main__":
    hacker_news()
