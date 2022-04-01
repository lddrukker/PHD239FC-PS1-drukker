import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import sys, os
import scipy.optimize as sp
import seaborn as sns
from pathlib import Path 
from tabulate import tabulate
import math
from sympy import symbols, Eq, solve
from scipy.optimize import fsolve
import datetime

# Define functions
def date_form(date):
    date_str = np.array2string(date)
    year = np.int64(date_str[0:4])
    month = np.int64(date_str[4:6])
    day = np.int64(date_str[6:])
    return([year,month,day])

def actual360(date):
    dates = date_form(date)
    year = dates[0]
    month = dates[1]
    day = dates[2]
    # Hard code in the beginning date
    date_begin = datetime.date(2019,3,4)
    date_actual = datetime.date(year,month,day)
    # Return actual/360
    days_num = date_actual - date_begin
    year_frac = days_num.days/360
    return(year_frac)

def isda_30i_360(date):
    dates = date_form(date)
    year = dates[0]
    month = dates[1]
    day = dates[2]
    # Apply 30i/360 day correction
    if day==31:
        day=30
    # Hard code in the beginning date
    year_begin = 2019
    month_begin = 3
    day_begin = 4 
    # Return 30i/360
    days_num = (year-year_begin)*360 + (month-month_begin)*30 + day-day_begin
    year_frac = days_num/360
    return(year_frac)

# pathlib allows us to set the paths while
# automatically adjusting for the OS
py_path = Path.cwd()
Output_PATH = py_path.parent.joinpath('Output')
Data_PATH = py_path.parent.joinpath('Data')

# Read in data
output = pd.read_excel(Data_PATH.joinpath("libor_rates_output_022819.xlsx"),engine='openpyxl')

output["yrs_actual"] = 0
for i in range(1,200):
    output.loc[i,"yrs_actual"] = actual360(output.loc[i,"Date"])
    #output.loc[i,"yrs_30i360"] = isda_30i_360(output.loc[i,"Date"])


# Loop over different tau values and find the tau values that minimize RMSE
output["X1"] = 0
output["X2"] = 0
output["X3"] = 0
output["yhat"] = 0

T1 = 1
T2 = 1
min_mse = 999999999

for tau1 in np.arange(0.5,0.7,0.01): # After many iterations these look to be the ranges to target
    for tau2 in np.arange(14,16,0.1):
        for i in range(1,200):
            T = output.loc[i,"yrs_actual"]
            output.loc[i,"X1"] = (1-np.exp(-T/tau1))/(T/tau1)
            output.loc[i,"X2"] = (1-np.exp(-T/tau1))/(T/tau1) - np.exp(-T/tau1)
            output.loc[i,"X3"] = (1-np.exp(-T/tau2))/(T/tau2) - np.exp(-T/tau2)

        mdl = sm.OLS(output["Zero Rate"][1:],sm.add_constant(output[["X1","X2","X3"]][1:])).fit()
        mse = mdl.mse_resid

        if mse<min_mse:
            T1=tau1
            T2=tau2
            betas = mdl.params
            output["yhat"] = sm.add_constant(output[["X1","X2","X3"]][1:]) @ betas

            min_mse = mse

print("Selected tau1 is ", T1)
print("Selected tau2 is ", T2)
print("Betas are \n", betas.T)
print("Min MSE is ", min_mse)

print(output)

text_file = open(Output_PATH.joinpath("q8i"), "w")
text_file.write(str(round(T1,2)))
text_file.close()

text_file = open(Output_PATH.joinpath("q8ii"), "w")
text_file.write(str(round(T2,2)))
text_file.close()

#text_file = open(Output_PATH.joinpath("q8iii"), "w")
#text_file.write(tabulate(betas,tablefmt="latex"))
#text_file.close()

text_file = open(Output_PATH.joinpath("q8iv"), "w")
text_file.write(str(min_mse))
text_file.close()

text_file = open(Output_PATH.joinpath("q8va"), "w")
text_file.write(output.loc[0:49].to_latex(index=False))
text_file.close()
text_file = open(Output_PATH.joinpath("q8vb"), "w")
text_file.write(output.loc[50:99].to_latex(index=False))
text_file.close()
text_file = open(Output_PATH.joinpath("q8vc"), "w")
text_file.write(output.loc[100:149].to_latex(index=False))
text_file.close()
text_file = open(Output_PATH.joinpath("q8vd"), "w")
text_file.write(output.loc[150:199].to_latex(index=False))
text_file.close()


