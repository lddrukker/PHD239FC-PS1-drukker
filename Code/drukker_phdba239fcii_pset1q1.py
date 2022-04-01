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
apr = 0.0525
r = apr/12
mat_mon = 360
mat_yr = 30
P = 1000000

#### 1.a
#c = P * r / (1+r-(1/(1+r))**360)
c = P * r / (1 - 1/(1+r)**360)
C = str(round(c,2))
#print('Monthly payments are $', C)

# Output
#with open(Output_PATH.joinpath('q1a.tex'),'w') as tf:
#    tf.write(tabulate(np.reshape(c,(1,1)),tablefmt="latex", floatfmt=".2f"))
    #tf.write(c.to_latex())
text_file = open(Output_PATH.joinpath("q1a"), "w")
text_file.write(C)
text_file.close()


#### 1.b
#pv = c/r * (1+r-(1/(1+r))**260)
pv = c/r * (1-1/(1+r)**260)
PV = str(round(pv,2))
#print('Present value of remaining balance is $', PV)

# Output
text_file = open(Output_PATH.joinpath("q1b"), "w")
text_file.write(PV)
text_file.close()


#### 1.c
b108 = c/r * (1-(1/(1+r))**252) #* (1+r)**12
b120 = c/r * (1-(1/(1+r))**240)

b_diff = b108-b120
payments = c*12
interest = (payments-b_diff )

b108 = str(round(b108,2))
b120 = str(round(b120,2))
b_diff  = str(round(b_diff,2))
payments = str(round(payments,2))
interest = str(round(interest,2))

# Output
text_file = open(Output_PATH.joinpath("q1ci"), "w")
text_file.write(b108)
text_file.close()

text_file = open(Output_PATH.joinpath("q1cii"), "w")
text_file.write(b120)
text_file.close()

text_file = open(Output_PATH.joinpath("q1ciii"), "w")
text_file.write(b_diff)
text_file.close()

text_file = open(Output_PATH.joinpath("q1civ"), "w")
text_file.write(payments)
text_file.close()

text_file = open(Output_PATH.joinpath("q1cv"), "w")
text_file.write(interest)
text_file.close()

