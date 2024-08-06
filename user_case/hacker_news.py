import os

# If you are a VS Code users:
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppys.pp.mei import Mei

# Change the API key to your own
# os.environ["OPENAI_API_KEY"] = ""


def hacker_news_action_flow(self, url):

    self.do_check(f"go to the given {url}, save the page's HTML", show_response=True)

    self.do_check("show the top 10 news @llm, and send it to me", show_response=True)

    self.do_check("pick the news that related to Large Language Models, summarize all the news, and send it to me", show_response=True)



hacker_news = Mei(hacker_news_action_flow)

hacker_news.run(url="https://news.ycombinator.com/")

# Debugging mode
# command_line_results = hacker_news.test_run(
#     node_num=-1,
#     num_of_action=2,
#     handle_exceptions=False,
#     max_length=1000,
#     use_command_line=True
# )
# print(f"command_line_results: {command_line_results}")

# inline_results = hacker_news.test_run(
#     node_num=-1,
#     num_of_action=3,
#     handle_exceptions=False,
#     max_length=40,
#     use_command_line=False,
#     updates = {"actionflow.history_codes":["a = 1"]})
# print(f"inline_results: {inline_results}")
