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
f1_001 = 0.11
f1_012 = 0.13
f1_023 = 0.17
P = 1000

#### 3
r01 = f1_001
r02 = ((1+f1_012)*(1+r01))**(1/2) - 1
r03 = ((1+f1_023)*(1+r02)**2)**(1/3) - 1

# Output
text_file = open(Output_PATH.joinpath("q3i"), "w")
text_file.write(str(round(r02,4)))
text_file.close()

text_file = open(Output_PATH.joinpath("q3ii"), "w")
text_file.write(str(round(r03,4)))
text_file.close()