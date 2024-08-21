# If you are a VS Code users:
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppys.pp.mei import Mei


def hacker_jobs_action_flow(self, url):

    self.do_check("go to the given url, show the HTML", show_response=True)

    self.do_check("transform the HTML to text, save the text", show_response=True)

    self.do_check("Split the text to several chunks, and make sure every chunk is within 3000 words", show_response=True)

    self.do_check("from the text of each chunk, show jobs located at UK @llm, gather all summary and send it to me", show_response=True, show_prompt=False)


hacker_news = Mei(value=hacker_jobs_action_flow)

hacker_news.run(url="https://news.ycombinator.com/item?id=40846428")
