# ActionFlow

We've just briefly introduced `actionFlow`, but it's not comprehensive enough. Here, we'll focus on the three parts of actionFlow: 

`actionFlowPending`,

 `actionFlowCurrent`
 
 `actionFlowHistory`,
 
 and their logic:

![alt text](/assets/actionFlowPipeline.png)

## How to represent the actionFlow?

How to represent the actionFlow, by JSON or by Python?

The answer is both. **JSON** and **Python code** can BOTH represent an actionFlow(but I recommend to use JSON because it contains more information)

If you define your agent's actionFlow by Python, the agent would **translate the Python code into JSON**.

For example:


Translate: **ActionFlow in Python code**

```python
@puppy1.main_thread
def actionFlow:
    ## search for the NBA game
    search_content = 'What NBA game is available'
    searchResults = self.GoogleSearch.run(search_content)

    ## send the price to me
    puppy1.do()


puppy1.run()
```

into: **ActionFlow in JSON**

```python
actionFlow=[{'action': 
'search for the NBA game', 

'code':
"""
## search for the NBA game
search_content = 'What NBA game is available'
searchResults = self.GoogleSearch.run(search_content)"""

'status': 
'fixed'  },

{'action': 
'send the price to me', 

'code':
"""
## send the price to me
puppy1.do()
""",

'status':
'semi-fixed'
},
]
```

## What's the logic behind the actionFlow?

