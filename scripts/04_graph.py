import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#import plotly.express as px
import sys

def main():
 
    df=pd.read_csv('output.csv', header=0)
    df['MIPS']=df['instructions']/df['time']/1000000
    sns.set(font_scale=2)
    # #scatterplot
    sns.scatterplot(data=df, x="MIPS", y="power/energy-pkg/", hue='Appname', style="Turbo Mode", s=150, markers= ['s','*'] )  
    plt.gcf().set_size_inches((16, 9)) #resize
    #place legend outside top right corner of plot
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0,markerscale=2)
    plt.savefig('power.png', bbox_inches="tight")
    plt.show()
    
    #boxplot
    #sns.boxplot(x="Appname", y="time",hue="Turbo Mode", data=df)
    sns.catplot(x="Appname", y="time",hue="Turbo Mode",kind="violin", data=df)
    plt.gcf().set_size_inches((16, 9)) #resize
    plt.ylim(0, 100)
    #plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.show()
    plt.savefig('time_app.png')
if __name__ == "__main__":
    main()