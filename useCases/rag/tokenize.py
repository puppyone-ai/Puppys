import tiktoken
import os

class TikTokenizer:
    def __init__(self, model_name='gpt-4-turbo'):
        self.tokenizer = tiktoken.encoding_for_model(model_name)

    def tokenize(self, text):
        tokens = self.tokenizer.encode(text)
        return tokens


if __name__ == "__main__":
    tokenizer = TikTokenizer()
    tokens = tokenizer.tokenize("This is an example sentence.")
    print(tokens)