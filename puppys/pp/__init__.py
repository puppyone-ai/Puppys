r"""
In general cases, users will only provide descriptions of what they want to achieve 
but will not give specific instructions on how to achieve the goal.
The agents will then have to figure out how to achieve these goals.
For example, if we want the agent to design a poster for us and 
already provide enough information about what we want, 
there are still many possible ways for the agent to do the task. 
It could generate an HTML (webpage) file and convert it to a PDF. 
It may also write some XML (a general marking language) in the format of Microsoft Word and send us a poster in .docx format, 
or more directly, output some .svg (vector graph) source code so we have a vector graph poster right there. 
In this case, the simple task of "poster designing" can be accomplished 
in many different ways, and each of these options has its pros and cons. 
In more complicated tasks, the agent may take several steps to solve a problem 
and need to make a decision in each step. 
The space for possible combinations of actions will be huge, 
and it is hard for the agent to decide which approach to take.
"""