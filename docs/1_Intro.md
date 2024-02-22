# Before Building your agent

**What language do agents speak?**

When an agent to plan, what language does it use for reasoning? Is it **natural language**, or **code language**? 

This is a question worth pondering. The answer from current agent frameworks is **natural language**, and the code language only interact with natural language, but don't play a role while planing. Such as AutoGen and Auto-GPT, as following:

![alt text](/assets/N2N.png)

However, **That's far not enough**

In fact, a LLM based agent consists of three parts: 

1. sensing the environment. 
>for example: *There are three chairs in the room.*

1. making decisions:


2. executing actions.


 Sensing the environment often relies on natural language, such as stating 'There are three chairs in the room.' Execution, however, is usually conducted through code, like print(\"hello world\"). Hence, agent planning necessarily involves both natural language and code language. Relying on only one of these is inadequate
 
Therefore we introduce **Puppys**.

![alt text](/assets/NC2NC.png)


the symbol of cross-over with a circle is [*Kronecker product*](https://en.wikipedia.org/wiki/Kronecker_product), it's a term in physics and math. 

What about after inducing version language?

![alt text](/assets/NCV2NCV.png)

## The philosophy behind it

Condensed matter and quantum mechanics corresponse two different languages. The former is 

Building an [*Grand Unified Theoretical*](https://en.wikipedia.org/wiki/Grand_Unified_Theory#:~:text=Grand%20Unified%20Theory%20(GUT)%20is,GUT%20models%20theorize%20its%20existence.) agent framework is so damn difficult.

![alt text](/assets/env&func.png)