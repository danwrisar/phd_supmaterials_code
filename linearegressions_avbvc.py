# Packages used
import pandas as pd # For reading csv files containing gas use data
import seaborn as sns # For creating linear regression graphs
sns.set("notebook") # Linear regression graph colour scheme
import matplotlib.pyplot as plt # For modifying and standardising the X and Y-axis ticks in the linear regression graphs
from array import * # For use in the loop function

# Specify the identifiers to be used in the loop. In this example, participants 1 - 4 all have data intact for two experimental periods, while only 1 - 3 also have data intact for a third experimental period.
abserials = [1,2,3,4]
abcserials = [1,2,3]
serlist = abcserials # Define the list of participants to be used in the loop

# Specify sources
datasource = pd.read_csv(r'XXXX\{}_gasuseprepared.csv'.format(str(x), low_memory = False, keep_default_na=False)) # Replace XXXX with file path and replace '_gasuseprepared.csv' with filename. This is a pre-prepared csv in the format of 
datasavelocation = (r'XXXX\{}_gasuseprepared_wConditions.csv'.format(str(x))) # Location to which a new csv will be saved following stacking of dataset and adding condition labels based on columns
graphsavelocation = (r'XXXX\{}_gas_lr_graph.csv'.format(str(x))) # This is where each linear regression graph will be saved.

# Loop
for x in serlist:
    df = datasource
    savedf = datasavelocation
    save_hueregression_under155_ab = graphsavelocation
       
    # Reformat columns
    df.columns = pd.MultiIndex.from_tuples([tuple(c.split('_')) for c in df.columns]) # Stacks the columns from a wide dataset to a long dataset which enables the graphing
    df = df.stack(0).reset_index(1) 

    # Rename column and replace values
    df.rename(columns={'level_1':'Year'}, inplace=True)
    df.Year[df.Year == 'YA'] = 'Year A'
    df.Year[df.Year == 'YB'] = 'Year B'
    df.Year[df.Year == 'YC'] = 'Year C'
    
    # Save new csv
    df.to_csv(savedf)

    # Uncommnet the below if needing to remove all rows where average air tempearture temperature is over 15.5C
    # df_fix = df[df['AvgT'] < 15.5]
        
    # PLOT THE CHART THAT COMPARES EACH SERIAL ON ONE WITHOUT >15.5C
    lm = sns.lmplot(x="AvgT", y="kWh", hue="Year", data=df_fix, palette="Set1", markers=['o', 'x', 's'], scatter_kws={"alpha":0.7}, size=9, aspect=0.7, legend=False)

    # Change the titles of the plots and specify limitations and ticks for axes
    fig = lm.fig
    a1 = fig.axes[0]
    a1.set_title("")
    plt.ylabel("Total daily gas use (kWh)")
    plt.ylim(-10, 360)
    plt.xlabel("Average daily outdoor temperature (\xb0C)")
    plt.xticks([-5.0,-2.5,0,2.5,5.0,7.5,10.0,12.5,15.0,17.5])
    lm.ax.legend(loc=1)
    lm.savefig(save_hueregression_under155_ab)
    
    print('Participant {} graphing complete!'.format(x)) # Use this command to return that each serial number of interest has been processed successfully/
