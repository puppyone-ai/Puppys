def decisiontree(self):
    self.do_check(f"go to the given {url}, save the page's HTML", show_response=True)
    # To show the top 10 news, I will use the LLM to extract and summarize the top news from the HTML content of the webpage.
    prompt = "Extract and summarize the top 10 news from this HTML content: " + html_content
    top_10_news = llm(prompt=prompt)
    
    # To extract news related to Large Language Models from the top 10 news summary, I will use the LLM to find and summarize.
    prompt_related_news = "From the following news summary, extract and summarize all news related to Large Language Models: " + top_10_news
    related_news_summary = llm(prompt=prompt_related_news)
    
    # Now, I will send the summarized news related to Large Language Models to the user.
    talk_with_human(message=related_news_summary)
    
    
