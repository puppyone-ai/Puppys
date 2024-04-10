import sys
import os
from puppy import Puppy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use mllm to change mode, example: Mei = Puppy(name="Mei", mllm=True), @mllm rather @gpt

hacker_news = main_thread
@hacker_news.actionflow
def pending():

    """
    Read the hackernews and show the top 10 news name and their urls based on the HTML
    """

    ## go to this website:https://news.ycombinator.com/ , save its HTML. @python
    Mei.do()
    print(HTML_text)

    ## show the top 10 news name and their urls based on the HTML @gpt, and send the message to the user
    Mei.do()
    print(news_and_urls)

hacker_news.run()

hacker_news.actionflow.pending=[{name:,code:,status:,}]

@hacker_news.create_function
def callPeople():
    print("hello,motherfucker!")

def xxx():
    print("hello,motherfucker!")
hacker_news.callPeople()=xxx()

def my_task():
    ...
    read_hackernews()
    Mei.peep_hackernews.experience
    ...

@Mei.peep_hackernews
def find_hottest():

    ## define the hottes 2 news based on the news.
    Mei.do()

@Mei.peep_hackernews
def find_hottest_hackernews():


    Mei.retrieve()

    ## Read the hackernews and show the top 10 news name and their urls based on the HTML

    Mei.do()

    ## define the hottes 2 news based on the news.
    Mei.do()

main_thread.run()

@Mei.broswer_hackernews
def browser_news():

    ## open the browser and search for the news
    Mei.read_hackernews()
    Mei.do()

    ## checke evry news and deliver the news to the user
    print(news)

Mei.run(thread = 'broswer_hacknews')

@Mei.food_delivery
def check_resturaunts():

    ## check the resturaunt which is selling the pizza
    Mei.do()
    print(pizza)

@Mei.food_delivery
def order_pizza():

    ## read the resturaunt
    check_resturaunts()

    ## order the pizza
    Mei.do()
    print(order)

Mei.run(thread = 'peep_hacknews')
Mei.run(thread = 'food_delivery')
Mei.run('browser the hackernews and search for 2 hottest one and read it to me,\
         and order a pizza for me')


# TODO
# fixed the bug of saving actionflow_history
