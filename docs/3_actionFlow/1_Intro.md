# Intro of actionFlow
From a behaviorist perspective, if we define the behavior of an agent, then we have defined the agent itself.

This gives us an insight: defining an agent is essentially telling an agent step by step what to do（Although this is far from sufficient）. we can follow this line of thought and we introduce:

`actionFlow` , recording an agent's pending actions, current action, and historical actions.



## What are involved in an action flow?

The `actionFlow` delineates how an agent should execute actions and what kinds of actions it should undertake. The relative positions of actions on the chain reveal the sequence in which the agent executes these actions.

 Consider an example, the task of "buy me an NBA game ticket"":

```python
["search for the NBA game",
"check the time of the game",
"check the ticket price",
"buy the ticket"]
``` 

Next, it is necessary to distinguish between actions that have already been executed, actions that are currently being executed, and actions that are to be executed in the future. Therefore, when we talk about actionFlow, we are talking about three parts:

`actionFlowPending`: actions that are scheduled to be executed in the future.

`actionFlowCurrent`: the action that is currently being executed.

`actionFlowHistory`: actions that have already been executed.

Using "buying me an NBA ticket" as an example, if the agent is currently checking the ticket price, then the three actions would be as follows:

```python
actionFlowHistory=[
"search for the NBA game",
"check the time of the game"
]

actionFlowCurrent=[
"check the ticket price"
]

actionFlowPending=[
"buy the ticket"
]
``` 

## More about an actionFlow
Here, we have discussed what should be included in actionFlow but have not yet covered the logic between the different parts of an action, nor the properties that actions within actionFlow possess. 

In the following pages, we will delve into the properties of an action,the default logic of actionFlow, and how to customize the properties and logic of actions.



## The philosophy behind it


