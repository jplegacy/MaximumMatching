
import math
from csvConstants import *

# --- Additional Columns --
def addMinusFirstPassTime(df):    
    df[MFPT_CN] = df[TIME_CN] - df.groupby(SOLVER_CN)[TIME_CN].transform('min')


def addCloseToCompleteMetric(df):
    metricColumn = []
    for d,n,m,t,to in zip(df[D_CN],df[N_CN],df[M_CN], df[TIME_CN], df[TIMEOUT_CN]):
        metricColumn.append(closeToCompleteMetric(n,m,d,t,to))

    df[CTC_CN] = metricColumn


def addTimeOutColumn(df):
    df[TIMEOUT_CN] = [df[TIME_CN].max()]*len(df)


# --- Metrics ---
def closeToCompleteMetric(n,m,d,t,to):
    return m/(n**d)


    