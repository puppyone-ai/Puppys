r"""
Sensing and adapting to the environment is another essential feature of intelligence. Sufficient information is a preliminary request for making good decisions.
However, in practice, agents may need more interfaces to retrieve the information from their environment. For example, when running a piece of script or compiling a binary for users, necessary dependencies and runtime for the code must be available. Yet, due to the ignorance of the local runtime, agents may unconsciously write some code that can't be executed and thus fail the task.
In more complicated situations, the agents must interact with a constantly varying environment. 
For example, the user may want the agent to perform trading in the stock market for profit. In this case, the agent can't predict the market and has to face risks directly.

The information of the environment faced by an agent can be encapsulated into an `Env` instance and pass to the agent.

"""

from .env import Env
from .func_env import FuncEnv
