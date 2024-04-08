
<img src="./assets/PuppyAgentHorizon.png" alt="Image">
*An open-source **Code-Native AI Agents** framework*

<div align="center">

[![Twitter Follow](https://img.shields.io/twitter/follow/PuppyAgentTech?label=PuppyAgent_Lab&style=social)](https://twitter.com/PuppyAgentTech) &ensp;
</div>

<div align="center">

**📜 [Document](https://mulberry-magician-e0a.notion.site/Puppys-document-83e2e55cfd27449589a6a721402ff4bc?pvs=4)**
&ensp;|&ensp;
**🔌 [Install](https://mulberry-magician-e0a.notion.site/Install-453ccfa356a04eda865c68e489d0e6bf?pvs=4)**
&ensp;|&ensp;
**⚽ [QuickStart](https://www.notion.so/Quick-Start-f4f383324012448180049f78035ccfa2)**

</div>

* **Code-Native**: Puppys is a code-native agent framework. Every dialog is code.
* **Multi-Threads**: Puppys enable you to build an agent with multi-thread.
* **Human-Agent Interacts**: Your agent will ask you when it cannot understand what you said.
* **tuning-machine-like agent**: program an agent by programming the agent's decision tree and its enviroment.


<div align="center">
<img src="./assets/tuning.png" alt="Image" width="500">
</div>

#### Quick Start

1. *Hacker News Reporter*

```
import sys
import os
from puppy import Puppy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# The name of agent is Mei
Mei = Puppy(name="Mei")


# change the API key to your own
os.environ["OPENAI_API_KEY"] = "Your_OpenAI_API_Key"


# define the agent's main thread's actionflow
@Mei.mainthread
def actionflow_pending():

    ## go to this website: "https://https://news.ycombinator.com/news/" , save its HTML. @python
    Mei.do()
    print(HTML_text)

    ## save the top 10 news name and their urls based on the HTML @gpt, and send the result to me
    Mei.do()


Mei.run()
```