# Actions

In the previous page, we briefly introduced the design philosophy of actionFlow, but we did not discuss **How to deal with actions**. Now let talk about action

`action` is an operation that needs to be executed on the `actionFlow`

## Properties of an action



In addition to knowing **what** action to execute, an agent also needs to know **how** to execute the action. For an LLM-based agent, executing an action essentially involves executing code. 

Therefore, we introduce the properties of an actions

`action`: the name of the action.

 `code` : the code that needs to be executed to complete the aciton.

 `status`: how to interpret the code.

 An example is as follows:

```python
action=
{'action': 
'search for the NBA game', 

'code':
"""
## search for the NBA game
search_content = 'What NBA game is available'
searchResults = self.GoogleSearch.run(search_content)"""

'status': 
'fixed'  }
``` 

Now we introduce the detail of each of the properties:


### code

For an LLM-based agent, executing an action essentially involves generating code and then running the code. Therefore, `code` is used to describe the specific code that needs to be run behind an action.

An example for the generated code is:

```python
## search for the NBA game
# use google search 
search_content = 'What NBA game is available'
searchResults = self.GoogleSearch.run(search_content
```

### status

In addition to specifying what code to run, 

`status` shows how agent need to compile before running the code. For one action, there are three default statuses:

1. **fixed**
   
   agent **cannot** either plan the action and decide how to execute this action
   - **Planning:** The agent is not involved in planning the action.
   - **Execution:** The agent is not involved in executing the action.

   use `##` to mark your planed action, and write code behind it to execute the action. Even though the agent is not involved in planning and executing the action, a good comment can help the agent to understand the context better, and therefore help the agent to plan and execute other action better.
   ```python
   ## clarify I am still running
   print("now i am here")
   google.gmail.send("i am still running")
   ```


2. **semi-fixed** 
   
   agent **cannot** plan the action but **can** decide how to execute this action
   - **Planning:** Humans specify the action.
   - **Execution:** The agent determines how to execute this specified action.

   please use `##` with comment to mark your planed action for the agent, and the `puppy.do()` is for agent to execute the action.
   ```python
   ## rethink about the answer @rethinker
   puppy.do()
   ```

3. **changeable** 
   
   Agent **can both** plan action and how to execute this action
   - **Planning:** The agent decides what action to take.
   - **Execution:**  The agent determines how to execute this specified action.

   Use `##` with no comment to mark this task is for agent to decide the action, and the `puppy.do()` is for agent to execute the action.
   ```python
   ## 
   puppy.do()
   ```




## More about an action


Currently we only set up the properties of `code` and `status`. But user can define your own properties for an action. But make sure you define how to interpret the properties.

## The philosophy behind it

> *Man is born free, and everywhere he is in chains*

When we talk about an autonomous agent, we might not necessarily mean to let it be entirely autonomous. (In fact, there's no such thing as a completely autonomous employee; you always have to teach him or her what to do at some point!)



![alt text](/assets/agent_with_fixed_actions.png)

Within an actionFlow, we might always need to insert some fixed actions, turning an agent with high freedom but unable to achieve any objectives into one with less freedom but capable of moving forward along a set path!