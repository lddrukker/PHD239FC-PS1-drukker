import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys, os
import scipy.optimize as sp
import seaborn as sns
from pathlib import Path 
from tabulate import tabulate

# pathlib allows us to set the paths while
# automatically adjusting for the OS
py_path = Path.cwd()
Output_PATH = py_path.parent.joinpath('Output')
data_path = py_path.parent.joinpath('Data')

# Initialize values
r01 = 0.05
r02 = 0.06
r03 = 0.07
P = 1000

#### 2.a
f1_012 = (1+r02)**2/(1+r01) - 1
f1_023 = (1+r03)**3/(1+r02)**2 -1 

# Output
text_file = open(Output_PATH.joinpath("q2ai"), "w")
text_file.write(str(round(f1_012,4)))
text_file.close()

text_file = open(Output_PATH.joinpath("q2aii"), "w")
text_file.write(str(round(f1_023,4)))
text_file.close()


#### 2.b
f1_013 = ((1+f1_012) * (1+f1_023)) - 1
borrow = P/(1+r01)
pay = borrow * (1+f1_013)

# Output
text_file = open(Output_PATH.joinpath("q2bi"), "w")
text_file.write(str(round(f1_013,4)))
text_file.close()

text_file = open(Output_PATH.joinpath("q2bii"), "w")
text_file.write(str(round(borrow,2)))
text_file.close()

text_file = open(Output_PATH.joinpath("q2biii"), "w")
text_file.write(str(round(pay,2)))
text_file.close()

