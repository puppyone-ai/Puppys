import html2text
from puppy.environment.func import FuncBase


class HTML2Markdown(FuncBase):
    def __init__(self, *args, **kwargs):

        """
                {
                    "FuncBase": {
                        "name": "",
                        "intro": "",
                        "tag": "func",
                        "__env_instance": None,
                        "__func": None,
                        "__visibility": True
                    }
                }
        """

        super().__init__(*args, **kwargs)

        self.name = "html2markdown"
        self.func = self.html2markdown
        self.intro = """
        Script reformatting, use it when you want to transform the format of a script from html to markdown.

        For example:
        ## transform the html content to markdown
        
        {
        "code":"
        html_content = \"\"\"
        <div>
            <h1>Welcome to My Website</h1>
            <p>This is a sample paragraph with <a href="https://example.com">a link</a> and some <strong>bold text</strong>.</p>
            <ul>
                <li>List item one</li>
                <li>List item two</li>
            </ul>
        </div>
        \"\"\"
        markdown = html2markdown(html_content)",
        "result":"
        # Welcome to My Website

        This is a sample paragraph with [a link](https://example.com) and some **bold text**.
        
          * List item one
          * List item two
        "
        }
        """

    @staticmethod
    def html2markdown(html_content):

        # 创建一个 html2text 对象
        text_maker = html2text.HTML2Text()
        # 忽略链接中的包装
        text_maker.wrap_links = False
        # 不将链接转换为脚注
        text_maker.inline_links = True
        # 忽略图像
        text_maker.ignore_images = True
        # 忽略表格
        text_maker.ignore_tables = True

        # 使用 html2text 转换 HTML
        markdown = text_maker.handle(html_content)

        return markdown


if __name__ == "__main__":
    # HTML 字符串
    html = """
    <div>
            <h1>Welcome to My Website</h1>
            <p>This is a sample paragraph with <a href="https://example.com">a link</a> and some <strong>bold text</strong>.</p>
            <ul>
                <li>List item one</li>
                <li>List item two</li>
            </ul>
        </div>
    """
    html2markdown = HTML2Markdown()
    print(html2markdown.run(html))
