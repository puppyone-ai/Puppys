# ActionFlow

`actionFlow` is like a to-do list for an agent, telling it the exact steps to follow: do this first, then do that. This way, an agent can take things step by step, just like running through a list of commands in a script.

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

However, if you allow the agent to generate the entire action flow on its own, it might omit some steps while planning. For instance, it might forget to check the ticket price, leading you to break down. To avoid this, we add a property of "fixed"  to the "check the ticket price" action. This ensures that the agent will always consider this step during the planning phase. Additionally, we have incorporated "code" into each action to ensure that the agent can execute the action by Python code.

```python
actionFlow=[{'action': 'search for the NBA game', 'status': 'semi-fixed', 'code': '# I need to know what game is available'}, 
           {'action': 'check the time of the game', 'status': 'semi-fixed', 'code': 'I need to know when the game is'}, 
           {'action': 'check the ticket price', 'status': 'fixed', 'code': 'I need to know how much the ticket is'},
           {'action': 'buy the ticket', 'status': 'semi-fixed', 'code': 'Finally, I need to buy the ticket'}]
``` 

## How to represent the actionFlow? (by natural language or by code)

The answer is both. It's imposite to fully represent an actionFlow only by natural language or only by code. It's because when we talked about XXX

Here we introduce the language to describe an actionFlow, we need to use both instead of one of them to run an agent: **JSON** and **Python code**


## ActionFlow in JSON:

```python
actionFlow=[{'action': 'search for the NBA game', 'status': 'semi-fixed', 'code': '# I need to know what game is available'}, 
           {'action': 'check the time of the game', 'status': 'semi-fixed', 'code': 'I need to know when the game is'}, 
           {'action': 'check the ticket price', 'status': 'fixed', 'code': 'I need to know how much the ticket is'},
           {'action': 'buy the ticket', 'status': 'semi-fixed', 'code': 'Finally, I need to buy the ticket'}]
``` 

## ActionFlow in Python code:

```python
@puppy1.action
def ReAct(task="provide the answer to the input question"):   
   ## search for the quesiton @google search @wiki search
   puppy1.do()

   ## rethink about the answer @rethinker
   puppy1.do()

   ## clarify I am still running
   print("now i am here")

   ## 
   puppy1.do()
   
puppy1.run()
```

## The philosophy behind it
