import os
from puppys.pp.main import Puppy
from puppys.env.func_env import FuncEnv
from puppys.pp.actions.explore import explore
from puppys.decorator import new_func


@new_func()
def firecrawl_browser_func(url:str, api_key=None):

    if api_key is None:
        api_key=os.environ["FIRECRAWL_API_KEY"]

    """
    Use it when you have a given web page that you need to browse. Return as markdown.

    for example:
    ## go to product hunt web page
    page_markdown = firecrawl_browser(url="https://www.producthunt.com/") # the url is essential
    """
    from firecrawl.firecrawl import FirecrawlApp

    app = FirecrawlApp(api_key=api_key)

    # Scrape a website:
    scrape_result = app.scrape_url(url)

    return(scrape_result['markdown'])



if __name__ == "__main__":
    result=firecrawl_browser_func(url="https://www.producthunt.com/")
    print(result)