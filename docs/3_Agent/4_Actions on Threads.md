# Actions on Threads






## The philosophy behind it

In our observation of human society, we can draw a bit of inspiration. In human societies, for a project, the stages of **planning**, **executing**, and **acceptance** are typically separate. Moreover, these stages are often carried out by three different individuals. 

Why is has to be like this? Imagine that if you are both planning and executing, you might make the plan overly simple if you are inclined to be lazy, allowing you to exert less effort during execution. And what if you are both executing and inspecting? You might feel during the inspection that you have already done a lot, and that what has been accomplished is sufficient. Therefore, it's essential that these three modules are handled by different individuals. In the context of an Agent, these three actions should be executed by different actions. It's crucial to avoid merging these three functionalities in a single recall of an LLM.