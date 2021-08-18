import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#import plotly.express as px
import sys

def main():
 
    df=pd.read_csv('output.csv', header=0)
    df['MIPS']=df['instructions']/df['time']/1000000
    sns.scatterplot(data=df, x="MIPS", y="power/energy-pkg/", hue='Appname', style="Turbo Mode") 
    # Move the legend to an empty part of the plot

    plt.gcf().set_size_inches((15, 10)) 
    plt.savefig('power.png', bbox_inches="tight")
    plt.show()
    #boxplot
    sns.boxplot(x="Appname", y="time",hue="Turbo Mode", data=df)
    plt.show()
    plt.savefig('time_app.png')
if __name__ == "__main__":
    main()