# Packages used
import pandas as pd # For reading csv files containing gas use data
import seaborn as sns # For creating linear regression graphs
sns.set("notebook") # Linear regression graph colour scheme
import matplotlib.pyplot as plt # For modifying and standardising the X and Y-axis ticks in the linear regression graphs

#### Convert serials to strings and then list
#totaldf['Serial'] = totaldf['Serial'].astype(str)
abserials = [15,17,24,45,83,89,123,128,147,190,202,204,205,208,245,249,253,275,287,302,322,354,359,378]
abcserials = [15,17,24,45,83,89,128,202,204,205,208,245,249,253,287,302,354]
test = [359]

# Send array to list
from array import *
serlist = test

# Loop
for x in serlist:
    df = pd.read_csv('E:\\Dan\\OneDrive - Loughborough University\\00_PEZCA\\06_Data\\Households\\Household_EnergyAnalysis\\{}_GasTemp_Regression.csv'.format(str(x), low_memory = False, keep_default_na=False))
    savedf = ('E:\\Dan\\OneDrive - Loughborough University\\00_PEZCA\\06_Data\\Households\\Household_EnergyAnalysis\\{}_GasTemp_Regression_Conditions.csv'.format(str(x)))
    save_hueregression_under155_ab = ('E:\\Dan\\OneDrive - Loughborough University\\00_PEZCA\\06_Data\\Figures\\gasuseabc\\{}_hueregression_under155_AvBvC.png'.format(str(x)))
    
    # Reformat columns
    df.columns = pd.MultiIndex.from_tuples([tuple(c.split('_')) for c in df.columns])
    df = df.stack(0).reset_index(1)

    # Rename column and replace values
    df.rename(columns={'level_1':'Year'}, inplace=True)
    df.Year[df.Year == 'YA'] = 'Year A'
    df.Year[df.Year == 'YB'] = 'Year B'
    df.Year[df.Year == 'YC'] = 'Year C'
    
    # Remove Year HSXPre and HSXPost from the df as we won't be using
    df = df[df.Year != 'HSXPre']
    df = df[df.Year != 'HSXPost']

    # Save new csv
    df.to_csv(savedf)

    # REMOVE ALL ROWS WHERE AVERAGE AIR TEMPERATURE IS OVER 15.5C
    df_fix = df[df['AvgT'] < 15.5]
    
    # PLOT THE CHART THAT COMPARES EACH SERIAL ON ONE WITHOUT >15.5C
    lm = sns.lmplot(x="AvgT", y="kWh", hue="Year", data=df_fix, palette="Set1", markers=['o', 'x', 's'], scatter_kws={"alpha":0.7}, size=9, aspect=0.7, legend=False)

    # Change the titles of the plots
    fig = lm.fig
    #fig.suptitle("Comparing daily total gas use to mean average daily air temperature (<15.5\xb0C) for Years A and B for serial number {}".format(str(serial)),y=1.05, fontsize = 14)
    a1 = fig.axes[0]
    a1.set_title("")
    plt.ylabel("Total daily gas use (kWh)")
    plt.ylim(-10, 360)
    plt.xlabel("Average daily outdoor temperature (\xb0C)")
    #plt.figure(figsize=(27, 15))
    plt.xticks([-5.0,-2.5,0,2.5,5.0,7.5,10.0,12.5,15.0,17.5])
    lm.ax.legend(loc=1)
    lm.savefig(save_hueregression_under155_ab)
    
    print('Participant {} graphing complete!'.format(x))
