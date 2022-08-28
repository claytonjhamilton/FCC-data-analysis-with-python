import pandas as pd
pd.options.mode.chained_assignment = None
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df['BMI'] = df['weight'] / ((df['height']/100)**2)
df['overweight'] = np.where(df['BMI'] > 25 , 1, 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = np.where(df['cholesterol'] == 1 , 0, 1)
df['gluc'] = np.where(df['gluc'] == 1 , 0, 1)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).size()
    df_cat = df_cat.rename(columns={'size': 'total'})

    # Draw the catplot with 'sns.catplot()'
    sns.catplot(data=df_cat, x='variable', y='total', col='cardio',kind='bar', hue='value')

    # Get the figure for the output
    fig = sns.catplot(data=df_cat, x='variable', y='total', col='cardio',kind='bar', hue='value').fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():

    # Clean the data
    df_heat = df
    df_heat = df_heat[
     (df_heat['ap_lo'] <= df_heat['ap_hi']) &
     (df_heat['height'] >= df_heat['height'].quantile(0.025)) & 
     (df_heat['height'] <= df_heat['height'].quantile(0.975)) &
     (df_heat['weight'] >= df_heat['weight'].quantile(0.025)) & 
     (df_heat['weight'] <= df_heat['weight'].quantile(0.975))
    ]

    df_heat.drop(['BMI'], axis=1, inplace=True)
  
    # Calculate the correlation matrix
    corr = df_heat.corr(method='pearson')

    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure
    fig, ax= plt.subplots(figsize=(24, 15))

    # Draw the heatmap with 'sns.heatmap()'
    sns.axes_style("white")
    sns.set(font_scale=1.4) 
    sns.heatmap(corr, 
                mask=mask,
                fmt='.1f',
                square=True,
                annot=True, 
                center=0.08,
                cbar_kws = {'shrink':0.5},
                linewidths=1
                
                # xticklabels=corr.columns.values,
                # yticklabels=corr.columns.values,
                # vmin=0,
                # vmax=.25, 
                # linewidths=.5,
            )

    plt.xticks(rotation=90) 
    plt.yticks(rotation=0) 

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
