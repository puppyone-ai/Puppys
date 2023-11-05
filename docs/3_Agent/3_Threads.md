# Threads

A thread dictates where an actionFlow should execute. If your task is simple, then actionFlow can run on a single thread. However, for complex tasks, you might need to set up multiple threads. On each thread, you assign different actionFlows, and all these threads work together to complete a task.


## Why Thread?

Some might wonder, why do we need to design multiple threads? Wouldn't actionFlow work just fine on a single thread? To this, we respond: For simple tasks, a single-thread can do the job. But as tasks get a bit more complex, we need a multi-threaded design. For instance, consider the reflexion agent that many are familiar with:

If you insisted to creat a reflexion agent with the task of draw a figure by python, you need to define the actionFlow like this:

```python
@puppy1.action
def ReFlecx(task="draw a figure of heart py python"):

    ## write the code
    puppy1.do()

    ## execute the code, and provide if the code runs correctly or not
    puppy1.do()

    ## reflect the code, if it's wrong, try to modify and run the code and run it, if after 3 times, the code is still wrong, then pass, and return "Sorry, I can't do it"
    try_times=0
    while try_times<3:
        if code_correct is Ture:
            pass
        else:
            # reflect the code, and modify the code
            puppy1.do()
            # run the code again 
            exec(code)

        try_times+=1
    if try_times>=3:
        message= "Sorry, I can't do it"
    else:
        return 'I have done it'

    ## 
    puppy1.do()
   
puppy1.run()
```

That is unreadable for both human and agent. However, if we use multi-thread, we can make the reflexion agent easier:

```python
@puppy1.action
def Main(task="draw a figure of heart py python"):   

    ## write the code
    puppy1.do()

    ## execute the code, and provide if the code runs correctly or not
    puppy1.do()

    ## try untill you made it
    puppy1.do()
   
@puppy1.reflex
def Reflex(planning='False'):

    ## if the code has been executed wrongly for 3 times, pulse the main thread, and return "Sorry, I can't do it"
    if try_times>=3:
        message= "Sorry, I can't do it"
        puppy1.action.pulse()
    else:
        puppy1.action.resume()

puppy1.run()
```

Certainly, you can add even more threads to give your agent additional capabilities, such as managing memory storage and retrieval, deciding when to bring in an external RAG, or determining when to send messages to other agents, even if agent safety: you can set up a "safety officer" thread that intervenes when the agent tries to execute potentially dangerous actions, like calling a destroying-world API (if it exists) or disclosing your personal privacy. This safety thread has the authority to interrupt other running threads to prevent such actions.

## The philosophy behind it

Think of it like the human brain. Our brain is divided into parts like the cerebral cortex, cerebellum, and brainstem. When the cerebral cortex is busy solving complex problems, the brainstem is taking care of the basics, like keeping our body temperature stable and making sure everything in the body runs smoothly.

The brainstem and cerebral cortex much like two separate threads in a computer program. The cerebral cortex's thread might be figuring out a math problem, while the brainstem's thread is ready to react if, say, you touch something hot.

Inspired by this, we've designed our framework with a similar idea in mind: actionFlow needs to be like the brainstem—running on its own thread, ready to handle tasks without waiting for the main problem-solving thread to finish its job. It's like when you're coding, and you have background processes that take care of updates or syncing without interrupting your main workflow. Just like everyone's familiar with background tasks in apps, that's how actionFlow should work.

