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
inputs  = pd.read_excel(Data_PATH.joinpath("libor_rates_input_022819.xlsx"),engine='openpyxl')
output = pd.read_excel(Data_PATH.joinpath("libor_rates_output_022819.xlsx"),engine='openpyxl')

inputs = inputs.drop(['Spread','Bid Spr Val', 'Ask Spr Val','Final Bid Rate','Final Ask Rate','Freq'], 1)


# Create mid
inputs["mid"] = inputs["Bid"]+(inputs["Ask"]-inputs["Bid"])/2

# Create dates for input and output data
inputs["yrs_actual"] = 0 
inputs["yrs_30i360"] = 0
for i in range(1,7):
    inputs.loc[i,"yrs_actual"] = actual360(inputs.loc[i,"Term"])
    inputs.loc[i,"yrs_30i360"] = isda_30i_360(inputs.loc[i,"Term"])
inputs.loc[0,"yrs_actual"] = (inputs.loc[1,"yrs_actual"]*360-90)/360
inputs.loc[0,"yrs_30i360"] = (inputs.loc[1,"yrs_30i360"]*360-90)/360

output["yrs_actual"] = 0 
output["yrs_30i360"] = 0
for i in range(1,200):
    output.loc[i,"yrs_actual"] = actual360(output.loc[i,"Date"])
    output.loc[i,"yrs_30i360"] = isda_30i_360(output.loc[i,"Date"])

# Create discount factor from forwards 
inputs["DCF"] = 1
inputs["rzero"] = 2.68217679185452/100
inputs["rzero_semi"] = 2.68217679185452/100
inputs.loc[0,"DCF"] = 1/(1 + (inputs.loc[0,"rzero"])*inputs.loc[0,"yrs_actual"])

for i in range(1,7):   
    #for j in range(1,i+1):
    f = inputs.loc[i,"mid"]/100 #inputs.loc[0,"mid"]/100 #
    ti = inputs.loc[i,"yrs_actual"]
    ti_1 = inputs.loc[i-1,"yrs_actual"]
    inputs.loc[i,"DCF"] = inputs.loc[i-1,"DCF"] / (1 + f * (ti-ti_1))
#inputs.loc[7,"DCF"] = 

#for i in range(7,)
# Create zero rates from discount factors
#inputs["rzero"] = inputs.loc[0,"mid"]/100 #0
for i in range(1,7):   
    k = 2
    ti = inputs.loc[i,"yrs_actual"] #inputs.loc[i,"yrs_30i360"]
    inputs.loc[i,"rzero_semi"] = k * ((1/inputs.loc[i,"DCF"])**(1/(k*ti)) - 1) #(1/inputs.loc[i,"DCF"]-1)/ti #
    inputs.loc[i,"rzero"] = (1/inputs.loc[i,"DCF"]-1)/ti #
#print(inputs)




# Create zero rates for actual dates of interest
# Linearly interpolate
output["rzero"] = 0 #inputs.loc[0,"rzero"]
output["DCF"] = 1
output.loc[1,"rzero"] = inputs.loc[0,"rzero"]
output.loc[1,"DCF"] = 1/(1 + output.loc[1,"rzero"]*output.loc[1,"yrs_actual"])
for i in range(2,7):
    rzero_L1 = inputs.loc[i-1,"rzero"]
    rzero_F1 = inputs.loc[i,"rzero"]
    date = output.loc[i,"yrs_actual"]
    date_L1 = inputs.loc[i-1,"yrs_actual"]
    date_F1 = inputs.loc[i,"yrs_actual"]
    output.loc[i,"rzero"] = rzero_L1 +(rzero_F1-rzero_L1)*(date-date_L1)/(date_F1-date_L1)
    output.loc[i,"DCF"] = 1/(1 + (output.loc[i,"rzero"])*output.loc[i,"yrs_actual"])
    rzero_L1 = inputs.loc[i-1,"rzero_semi"]
    rzero_F1 = inputs.loc[i,"rzero_semi"]
    output.loc[i,"rzero"] = rzero_L1 +(rzero_F1-rzero_L1)*(date-date_L1)/(date_F1-date_L1)



# Now work on long term parts
r = inputs.loc[7,"mid"]/100

# Account for the fact that the terms are in years now
inputs.loc[7,"DCF"] = (1 - r*inputs.loc[4,"DCF"]) / (1 + r)
inputs.loc[7,"rzero"] = (1/inputs.loc[7,"DCF"]-1)/inputs.loc[7,"Term"]
DCF_sum = inputs.loc[4,"DCF"]

for i in range(8,24):
    r = inputs.loc[i,"mid"]/100
    date_L1 = inputs.loc[i-1,"Term"] #inputs.loc[i-1,"yrs_30i360"]
    date_F1 = inputs.loc[i,"Term"] #inputs.loc[i,"yrs_30i360"]
    DCF_sum+= inputs.loc[i-1,"DCF"] * (date_F1-date_L1)
    inputs.loc[i,"DCF"] = (1-r*DCF_sum)/(1+r)
    #inputs.loc[i,"rzero"] =(1/inputs.loc[i,"DCF"]-1)/inputs.loc[i,"yrs_30i360"]
    inputs.loc[i,"rzero"] =(1/inputs.loc[i,"DCF"]-1)/inputs.loc[i,"Term"]
print(inputs)

for i in range(7,200):
    # Identify appropriate terms from inputs df
    t = output.loc[i,"yrs_30i360"]
    #print("t is ", t)
    term=0
    if t<=2:
        term=7
    else:
        for j in range(8,24):

            if inputs.loc[j,"Term"]>t: #and inputs.loc[j-1,"Term"]<=t:
                term=j
                break
            #else:
            #    continue
    #print("term is", term)
    if i<=199:
        # Identify rates and dates
        r_L1 = inputs.loc[term-1,"rzero"]
        r_F1 = inputs.loc[term,"rzero"]
        date_L1 = inputs.loc[term-1,"Term"]
        date_F1 = inputs.loc[term,"Term"]

        # Linearly interpolate
        r = r_L1 + (r_F1-r_L1)*(t-date_L1)/(date_F1-date_L1)
        output.loc[i,"DCF"] = 1/(1 + r*t)
        output.loc[i,"rzero"] = ((1/output.loc[i,"DCF"])-1)/t
    else:
        r = inputs.loc[23,"rzero"]
        output.loc[i,"rzero"] = 1/(1 + r*t)
        #output.loc[i,"rzero"] = ((1/output.loc[i,"DCF"])-1)/t

#output["rzero"] = (1+output["rzero"])**2-1

# Create forwards from discount factors for actual dates of interest
for i in range(0,199):
    dcf = output.loc[i,"DCF"]
    dcf_F1 = output.loc[i+1,"DCF"]
    date = output.loc[i,"yrs_30i360"]
    date_F1 = output.loc[i+1,"yrs_30i360"]
    output.loc[i,"forward"] = (dcf/dcf_F1 - 1) / (date_F1-date) * 100
print(output)
output = output[["Date","Zero Rate", "Forward Rate", "rzero","DCF","forward"]]

text_file = open(Output_PATH.joinpath("q6i"), "w")
text_file.write(output.loc[0:49].to_latex(index=False))
text_file.close()
text_file = open(Output_PATH.joinpath("q6ii"), "w")
text_file.write(output.loc[50:99].to_latex(index=False))
text_file.close()
text_file = open(Output_PATH.joinpath("q6iii"), "w")
text_file.write(output.loc[100:149].to_latex(index=False))
text_file.close()
text_file = open(Output_PATH.joinpath("q6iv"), "w")
text_file.write(output.loc[150:199].to_latex(index=False))
text_file.close()