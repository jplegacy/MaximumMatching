'''plotInterface.py

- Author: Jeremy Perez
- Course: CSC 489, Fall 2024
- Date: 10/19/24

Here's a CLI tool for parsing race csv. 

To get more information, try to run the file to get flag information

For a simple run, use the following:

python <path_to_this_file> <path_to_csv>

'''

import os
import pathlib

import seaborn as sns

from tools import *
sns.set_theme(style="whitegrid", font="Verdana", palette="pastel")

from csvConstants import *

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import pandas as pd
import argparse

from os import listdir
from os.path import isfile, join


def prepareData(args):
    """Creates the dataframe after parsing CSV file 

    Args:
        args (nameSpace): the arguments passed in

    Returns:
        tuple: (df, courseName)
    """

    # Case - When only a directory path is passed in
    if args.directory:
        DIRECTORYPATH = args.path
        filePaths = [f for f in listdir(DIRECTORYPATH) if isfile(join(DIRECTORYPATH, f))]

        assert len(filePaths) >= 1, "DIRECTORY IS EMPTY, PLEASE ENSURE THE LOCATION SPECIFIED IS CORRECT"
        
        frames = []

        for f in filePaths:
            frames.append(pd.read_csv(join(DIRECTORYPATH, f)))
            
        df = pd.concat(frames, ignore_index=True)
                      
        _, tail = os.path.split(DIRECTORYPATH)
        COURSENAME = tail

        return df, COURSENAME
    
    # Case - When only a file path is provided
    else:
        FILEPATH = args.path
        df = pd.read_csv(FILEPATH)

        _, tail = os.path.split(FILEPATH)
        COURSENAME = tail.split(".")[0]

        return df, COURSENAME

def refineData(df):
    df.drop_duplicates(subset=[TEST_PATH_CN,SOLVER_CN],keep="first", inplace=True)        
    
    df.drop(df[df[SUCCESS_CN]=='False'].index, inplace=True)
    
    # Leaves a single case where it timed out, so that it's expressed in the graph
    mask = df.duplicated(subset=[SOLVER_CN, SUCCESS_CN], keep='first') & (df[SUCCESS_CN] == "Timed Out")
    df.drop(index=df[mask].index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    addTimeOutColumn(df)
    addMinusFirstPassTime(df)
    addCloseToCompleteMetric(df)
        
def timeToSolvePlot(args, df, ax):
    if args.removeExcessRuntime:
        timeAxis = MFPT_CN
        xlabel = "Clock Time With First Success Runtime Removed in"

    else:
        timeAxis = TIME_CN   
        xlabel = "Wall Clock Time in"
    
    sns.ecdfplot(
                x=timeAxis,
                hue=SOLVER_CN,
                data=df,
                marker='o',
                markersize=3,
                stat='count',
                palette={name: color for (name, group), color in zip(groupsOfNames, mcolors.TABLEAU_COLORS)},
                ax=ax
                )

    # TIMEOUT LINE
    timeoutVal = df[TIMEOUT_CN].max()
    ax.axvline(x = timeoutVal, color="black", linestyle="--", linewidth=4)
    ax.text(timeoutVal+.1, 10,'Timeout',rotation=90,fontweight='bold')

    if args.logtime:
        ax.set_xscale('log') 
        xlabel += " log(s)"  
    
    else:
        xlabel += " (s)"  

    ax.set_xlabel(xlabel)
    ax.set_ylabel('Solved')
    ax.set_title("COURSE: " + COURSENAME)

def closeCompletePlot(args, df, ax):
    if args.removeExcessRuntime:
        timeAxis = MFPT_CN
        xlabel = "Clock Time With First Success Runtime Removed in log(s)"

    else:
        timeAxis = TIME_CN   
        xlabel = "Wall Clock Time in log(s)"
        
    sns.scatterplot(
        x=timeAxis,
        y=CTC_CN,
        data=df,
        hue=SOLVER_CN,
        palette={name: color for (name, group), color in zip(groupsOfNames, mcolors.TABLEAU_COLORS)},
        ax=ax,
        legend=False
    )

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel(xlabel)
    ax.set_ylabel('Partite Completeness Ratio')
    ax.set_title("Runtime to Completeness of Graph")
    
if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()

    parser.add_argument("path",  type=pathlib.Path, help = "Location to dataset")

    # Adding optional argument     
    parser.add_argument("-D", "--directory", action="store_true", help = "Specify whether the path is a directory to parse every file within it.")
    parser.add_argument("-d", "--display", default=True, type=bool, help = "Whether or not to Display Graph")
    parser.add_argument("-o", "--output", action="store_true", help = "Whether or not to output the graph to a file")
    parser.add_argument("-lt", "--logtime", action="store_true", help = "Whether or not to Use Logarithimic Time")
    parser.add_argument("-rmr", "--removeExcessRuntime", action="store_true", help = "Whether or not to subtract the earliest pass test from each runtime")

    # Parses input arguments
    args = parser.parse_args()

    # -------- PROGRAM STARTS HERE -------------------------

    df, COURSENAME = prepareData(args)    

    # REFINED DATA OVERWRITES VANILLA
    refineData(df)

    groupsOfNames = df.groupby(SOLVER_CN)

    f, (ax1, ax2)= plt.subplots(1,2, figsize=(16, 8)) # Width and Height of the chart
    
    timeToSolvePlot(args, df, ax1)
    closeCompletePlot(args, df, ax2)
    
    plt.tight_layout(h_pad=2)

    if args.output:
        currentFilePath = os.path.abspath(__file__)
        head, tail = os.path.split(currentFilePath)

        plt.savefig(head + "/graphs/" + COURSENAME + '.png')

    if args.display:
        plt.show() 


