# Quick Start

## Define your own agent

define a function with Decorator of XXX.action, where the XXX is the name of your agent. For example: 

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

We have defined three modes for each action. These three modes are created to distinguish between actions the agent can do independently, those it can't do by itself, but can do with human instruction, and those it cannot do at all:

1. **Agent-Plan&Act:**
   - **Planning:** The agent decides what action to take.
   - **Execution:**  The agent determines how to execute this specified action.
   please use ## TODO to mark this task is for agent to decide the action, and the puppy1.act() is for agent to execute the action.
   ```python
   ## TODO
   puppy1.do()
   ```

2. **Agent-Act Only:**
   - **Planning:** Humans specify the action.
   - **Execution:** The agent determines how to execute this specified action.
   use it via:
   ```python
   ## rethink about the answer @rethinker
   puppy1.do()
   ```

3. **Agent-Not Involved:**
   - **Planning:** The agent is not involved in planning the action.
   - **Execution:** The agent is not involved in executing the action.
   ```python
   ## clarify I am still running
   print("now i am here")
   ```


Once set up, you can start running it！

## The philosophy behind it

What exactly is an Agent? Is it something meant to focus on planning, taking action, or both? 

Well, it can be any of those. There's a bit of a puzzle here because we often try to put agents into neat little boxes: some are planners, others are doers, and some are a mix of both. A common approach is to separate the two: design agents that are either capable of planning only, action only, or both.

But wait a minute - aren’t we all born free, able to think and act as we please? That’s where the old way of designing agents falls short. It’s like telling a chef they can only cook but never plan a menu, or telling a pilot they can only fly but never map out the route.

The real question isn’t who can do what, but rather, what needs who to do it. It’s a small shift in thinking, but it makes a world of difference.

So, in our framework, we’ve tossed out the old rulebook. Permissions aren’t about the agent; they’re about the task or actions. When someone uses PuppyAgent to create their agent, we focus on what needs to be done, not on labeling the agent.