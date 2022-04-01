import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys, os
import scipy.optimize as sp
import seaborn as sns
from pathlib import Path 
from tabulate import tabulate
import math
from sympy import symbols, Eq, solve
from scipy.optimize import fsolve

# pathlib allows us to set the paths while
# automatically adjusting for the OS
py_path = Path.cwd()
Output_PATH = py_path.parent.joinpath('Output')
data_path = py_path.parent.joinpath('Data')

# Initialize values
c = 6 #0.06
y = 0.053
m = 10

# Calculate price
P = (c/2) / math.exp(y*(m-6)/12) + (100 + (c/2)) / math.exp(y*(m/12))
#print(P)
#print(math.exp(1))
#print(math.log(2.7183))

# Calculate forward rate

# Define symbols
#f2, f3 = symbols('f2 f3')
#f3 = symbols('f3')

# Define equation
f1 = 0.05
f2 = 0.0634
c2 = 0.04
c3 = c 

# Calculate f3
f3 = (math.log((100+(c/2))/(P - (c/2)/math.exp(f1*(m-6)/12))) - f1*5/12 - f2*(8-5)/12) * 12/(m-8)
#print(f3)

# Output
text_file = open(Output_PATH.joinpath("q5i"), "w")
text_file.write(str(round(P,4)))
text_file.close()

text_file = open(Output_PATH.joinpath("q5ii"), "w")
text_file.write(str(round(f3,4)))
text_file.close()


