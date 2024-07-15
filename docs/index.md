# Puppy
Framework for Plug-and-Play Agentic System

"""
*Hi puppy, fetch that ball for me!*
"""

## Install

```shell
pip install git+https://github.com/PuppyAgent/Puppys.git
```


## Quick Start & User Case

1. 📢 *Hacker News Reporter*

```python
from puppy.pp.mei import Mei

# change the API key to your own
# os.environ["OPENAI_API_KEY"] = ""

def hacker_news_decisiontree(self, url):

    self.do_check("go to the given url, show the HTML", show_response=True)

    self.do_check("show the top 10 news @llm, and send it to me", show_response=True, show_prompt=True)

    self.do_check("pick the news that related to Large Language Models, summarize all the news, and send it to me")


hacker_news = Mei(hacker_news_decisiontree)

hacker_news.run(url="https://news.ycombinator.com/")

```
