
<img src="./assets/PuppysHorizon.png" alt="Image">


<div align="center">

*Code-Driven AI Agentic system framework*

[![Twitter Follow](https://img.shields.io/twitter/follow/PuppyAgentTech?label=PuppyAgent_Lab&style=social)](https://twitter.com/PuppyAgentTech) &ensp;
</div>

<div align="center">

**📜 [Document](https://mulberry-magician-e0a.notion.site/Puppys-document-83e2e55cfd27449589a6a721402ff4bc?pvs=4)**
&ensp;|&ensp;
**🔌 [Install](https://mulberry-magician-e0a.notion.site/Install-453ccfa356a04eda865c68e489d0e6bf?pvs=4)**
&ensp;|&ensp;
**⚽ [QuickStart](https://mulberry-magician-e0a.notion.site/Quick-Start-f4f383324012448180049f78035ccfa2?pvs=74)**

</div>

* **Code-Driven**: The agent's thought and response are entirely code, instead of chat, meaning more interpretable and more controllable.
* **Plug and Play**: Agentic capabilities can be integrated into ANY part of your enterprise's codebase
* **Lite**: Minimal dependencies and minimal wrappers, mean that enterprises can develop flexibly and scalably.

<div align="center">

**-------------  🔥 Version 0.0.26 (30-May-2024):  -------------**

</div>

1. **Redesigned Grammar**: Now you use do(action) instead of ##action do().
2. **Supporting Parameters in Decisiontree**: parameter can be customized in decisiontree.
3. **Decouple Doing and Checking**: Checking and doing an action is different, now you can define them.
4. **Another User Case**: Playing Gotcha Game with 4 agents!

## Building an agent just like building a Turing machine

When programming an agent, what exactly are we programming?

We can draw some inspiration from the history of computer science. Consider a Turing machine:

We need to define its decision tree (finite state machine) and the environment (tape) in which the agent operates.

The advantage is that by defining a confined environment, we can effectively explore continuous learning within a specific domain.

<div align="center">
<img src="./assets/decisionTree_Enviroment.png" alt="Image" width="800">
</div>

## Hybrid solution of Agent and RPA

**Agents** can do tasks by themselves and work in many situations, but only be able to solve very simple problems.
**RPA** (Robotic Process Automation), on the other hand, can handle complex tasks but isn't very flexible. So, here is a question: **what if we make a hybrid agent that mix the advantages of agents and RPA?** Could this idea work?

Our solution is that, actionflow is as a list in the environment, which need to be interpreted by a decision tree.
Unlike previous agent frameworks, we placed the workflow within the environment, to be parsed by the decision tree, rather than a default flow.

Giving the agent a confined environment, and let the agent evolves in the confined environment.

<div align="center">
<img src="./assets/AgentRPA.png" alt="Image" width="800">
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
from puppy.pp.main import Puppy
from puppy.tools.usable_tools import UsableTools

# change the API key to your own
#os.environ["OPENAI_API_KEY"] = ""

def hacker_news_decisiontree(self):
    self.tool_box=UsableTools()

    self.do_check("go to https://news.ycombinator.com/ show the HTML")

    self.do_check("show the top 10 news, and send it to me")

    self.do_check("pick the news that related to Large Language Models, summarize all the news, and send it to me")


hacker_news = Puppy(decisiontree=hacker_news_decisiontree)

hacker_news.run()
```