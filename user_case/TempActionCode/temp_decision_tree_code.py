def decisiontree(self):
    self.do_check(f"go to the given {url}, save the page's HTML", show_response=True)
    # To show the top 10 news, I will use the llm function to process the HTML content and extract the top 10 news items.
    prompt = "Extract and summarize the top 10 news items from this HTML content: " + html_content
    top_10_news = llm(prompt=prompt)
    
    # To extract and summarize news related to Large Language Models from the HTML content, I will use the llm function.
    prompt_related_to_llm = "Extract and summarize all news related to Large Language Models from this HTML content: " + html_content
    summary_of_llm_related_news = llm(prompt=prompt_related_to_llm)
    
    # To send the summarized news to the user, I will use the talk_with_human function.
    talk_with_human(message=summary_of_llm_related_news)
    
    
