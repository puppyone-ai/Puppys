# ActionFlow
## What are involved in an action flow?

The `actionFlow` is a crucial attribute of an agent. It delineates how an agent should execute actions and what kinds of actions it should undertake. 

Imagine a chain composed of numerous actions; we refer to this as the "actionFlow." The relative positions of actions on the chain reveal the sequence in which the agent executes these actions. Consider the most simple example, with the task of "buy me a NBA game ticket"":

```python
actionFlow=["search for the NBA game",
            "check the time of the game",
            "check the ticket price",
            "buy the ticket"]
``` 

In this example, the agent should first search for the NBA game, then check the time of the game, and finally buy the ticket. 

However, if you allow the agent to generate the entire action flow on its own, it might omit some steps while planning. For instance, it might forget to check the ticket price, leading you to break down. To avoid this, we add a property of "fixed"  to the "check the ticket price" action. This ensures that the agent will always consider this step during the planning phase. Additionally, we have incorporated "reasoning" into each action to ensure that the agent fully understands the underlying intent behind each action during execution. The final actionFlow is illustrated below.

```python
actionFlow=[{'action': 'search for the NBA game', 'status': 'changable', 'reasoning': 'I need to know what game is available'}, 
           {'action': 'check the time of the game', 'status': 'changable', 'reasoning': 'I need to know when the game is'}, 
           {'action': 'check the ticket price', 'status': 'fixed', 'reasoning': 'I need to know how much the ticket is'},
           {'action': 'buy the ticket', 'status': 'changable', 'reasoning': 'Finally, I need to buy the ticket'}]
``` 

## How to represent the actionFlow? (JSON and Python code)

We have introduced JSON as a representation of an actionFlow. However, is JSON enough to express an actionFlow? The answer is NO.

Here we introduce two representations for actionFlow, we need to use both instead of one of them to run an agent: **JSON** and **Python code**

**JSON**
- **pro:** Easy to update, adeptness at handling real-life scenarios.
- **con:** still need to compile into code to be executable.


**Python code**
- **pro:** the most compatible format for agent execution. Support code interpretor.
- **con:** it’s not adept at managing real-life scenarios.Dificult to update.

Through testing, we found that the JSON mode is more effective for action global planning from the agent's perspective, while the Python code mode proves to be more efficient for executing individual actions.

## ActionFlow in JSON:

```python
actionFlow=[{'action': 'search for the NBA game', 'status': 'changable', 'reasoning': 'I need to know what game is available'}, 
           {'action': 'check the time of the game', 'status': 'changable', 'reasoning': 'I need to know when the game is'}, 
           {'action': 'check the ticket price', 'status': 'fixed', 'reasoning': 'I need to know how much the ticket is'},
           {'action': 'buy the ticket', 'status': 'changable', 'reasoning': 'Finally, I need to buy the ticket'}]
``` 

## ActionFlow in Python code:

```python
@puppy1.action
def ReAct(task="provide the answer to the input question"):   
   ## search for the quesiton @google search @wiki search
   puppy1.act()

   ## rethink about the answer @rethinker
   puppy1.act()

   ## clarify I am still running
   print("now i am here")

   ## TODO
   puppy1.act()
   
puppy1.run()
```

