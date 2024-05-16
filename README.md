
<img src="./assets/PuppysHorizon.png" alt="Image">


<div align="center">

*An open-source **Code-Native AI Agents** framework*

[![Twitter Follow](https://img.shields.io/twitter/follow/PuppyAgentTech?label=PuppyAgent_Lab&style=social)](https://twitter.com/PuppyAgentTech) &ensp;
</div>

<div align="center">

**📜 [Document](https://mulberry-magician-e0a.notion.site/Puppys-document-83e2e55cfd27449589a6a721402ff4bc?pvs=4)**
&ensp;|&ensp;
**🔌 [Install](https://mulberry-magician-e0a.notion.site/Install-453ccfa356a04eda865c68e489d0e6bf?pvs=4)**
&ensp;|&ensp;
**⚽ [QuickStart](https://www.notion.so/Quick-Start-f4f383324012448180049f78035ccfa2)**

</div>

* **Code-Native**: Puppys is a code-native agent framework. Every agent's action is code.
* **Multi-Threads**: Puppys enable you to build an agent with multi-thread.
* **Human-Agent Interacts**: Your agent will ask you when it cannot understand what you said.
* **turing-machine-like agent**: program an agent by programming the agent's decision tree and its environment.

<div align="center">

**-------------  🔥 Version 0.0.22 (14-May-2024):  -------------**

</div>

1. **Updated a New User Case**: A crypto data analysis, calculate BTC and ETH price.
2. **New Feature**: 'previewing_before_planning', a significant and default setting of Thread.
2. **Fixed bugs**: Fixed the bug parsing '##'.

<img src="./assets/dividerBlue.png" alt="Image">

## Hybrid solution of Agent and RPA

**Agents** can do tasks by themselves and work in many situations, but only be able to solve very simple problems.
**RPA** (Robotic Process Automation), on the other hand, can handle complex tasks but isn't very flexible. So, here is a question: **what if we make a hybrid agent that mix the advantages of agents and RPA?** Could this idea work?

Our solution is that, actionflow is as a list in the environment, which need to be interpreted by a decision tree.
Unlike previous agent frameworks, we placed the workflow within the environment, to be parsed by the decision tree, rather than a default flow.

Giving the agent a confined environment, and 

<div align="center">
<img src="./assets/AgentRPA.png" alt="Image" width="800">
</div>

## Building an agent just like building a Turing machine


When programming an agent, what exactly are we programming?

We can draw some inspiration from the history of computer science. Consider a Turing machine:

We need to define its decision tree (finite state machine) and the environment (tape) in which the agent operates.

The advantage is that by defining a confined environment, we can effectively explore continuous learning within a specific domain.

<div align="center">
<img src="./assets/decisionTree_Enviroment.png" alt="Image" width="800">
</div>


## Agent's planning: Talk is shit, show me your code!

When an agent perceives its environment, thinks, and acts, what language does it use? Is it **natural language**, or **code language**?

In fact, the biggest difference between an agent and an LLM is that **an LLM predicts the next token**, **an agent predicts the next action**. 

An action involves both the agent’s thoughts and decisions (natural language)and its execution  (code). Therefore, we made the atomic predicted unit of (natural language * code).
This prevents an agent from planning actions that it can never actually carry out.

<div align="center">
<img src="./assets/PuppyVsOthers.png" alt="Image" width="800">
</div>




## Quick Start & User Case

1. 📢 *Hacker News Reporter*

```
import sys
import os
from puppy.thread.main import Thread
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# change the API key to your own
#os.environ["OPENAI_API_KEY"] = ""

hacker_news = Thread()

@hacker_news.actionflow.update
def pending_list():

    ## go to https://news.ycombinator.com/ show me the HTML
    hacker_news.do()

    ## show the top 10 news @gpt, and send message to me
    hacker_news.do()

    ## pick the news that related to Large Language Models, summerize all the news, and show it to me
    hacker_news.do()

hacker_news.run()
```