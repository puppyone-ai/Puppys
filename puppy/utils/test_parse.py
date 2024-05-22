from puppy.utils.parse import parse_code2list



def test_parse():
    src = """
def pending_list():
    ## go to https://news.ycombinator.com/ show the HTML
    hacker_news.do()
    
    ## show the top 10 news @gpt, and send it to me
    hacker_news.do()
    
    ## pick the news that related to Large Language Models, summarize all the news, and show it to me
    hacker_news.do()    
"""
    res = parse_code2list(src)
    assert res[0].code.strip() == '## go to https://news.ycombinator.com/ show the HTML\nhacker_news.do()'
    assert res[1].code.strip() == '## show the top 10 news @gpt, and send it to me\nhacker_news.do()'
    assert res[2].code.strip() == '## pick the news that related to Large Language Models, summarize all the news, and show it to me\nhacker_news.do()'
    assert res[0].name == "go to https://news.ycombinator.com/ show the HTML"
    assert res[1].name == "show the top 10 news @gpt, and send it to me"
    assert res[2].name == "pick the news that related to Large Language Models, summarize all the news, and show it to me"