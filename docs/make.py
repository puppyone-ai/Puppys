## please help write this make,py to automate the documentation build process
import puppys
import os

os.system("pdoc puppys -t docs/ -o docs/ --logo '../../assets/PuppyAgentHorizon.png'")