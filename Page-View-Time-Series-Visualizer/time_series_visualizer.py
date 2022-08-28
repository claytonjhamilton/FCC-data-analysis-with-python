import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import pandas as pd
import seaborn as sns
import calendar
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data and use Pandas to import the data from "fcc-forum-pageviews.csv". Set the index to the date column.
df=pd.read_csv("fcc-forum-pageviews.csv").set_index('date')
df.index = pd.to_datetime(df.index)

# Clean the data by filtering out days when the page views were in the top 2.5% of the dataset or bottom 2.5% of the dataset.
df = df[
     (df['value'] >= df['value'].quantile(0.025)) & 
     (df['value'] <= df['value'].quantile(0.975))
    ]

def draw_line_plot():
  '''Create a draw_line_plot function that uses Matplotlib to draw a line chart similar to "examples/Figure_1.png". The title should be Daily freeCodeCamp Forum Page Views 5/2016-12/2019. The label on the x axis should be Date and the label on the y axis should be Page Views.
  '''  
  # Create figure and plot space
  fig, ax = plt.subplots(figsize=(12, 6))

  # Add x-axis and y-axis
  ax.plot(df.index.values,
       df['value'],
       color='red')

  # Set title and labels for axes
  ax.set(xlabel="Date",
       ylabel="Page Views",
       title="Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

  # Define the date format
  ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
  ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))

  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.reset_index(drop=False)
    df_bar['Years'] = pd.DatetimeIndex(df_bar['date']).year
    df_bar['Months'] = pd.DatetimeIndex(df_bar['date']).month

    df_bar = df_bar.groupby(['Years', 'Months'])['value'].mean().astype(int)
    df_bar = df_bar.unstack()

    # Draw bar plot
    fig = df_bar.plot.bar(legend=True
                         ,figsize=(9, 8) 
                   ).figure
    plt.ylabel('Average Page Views')
    plt.legend([calendar.month_name[x] for x in df_bar.columns.tolist()])
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    month_order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Year
    sns.boxplot(data=df_box, x='year',y='value',ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Month
    sns.boxplot(data=df_box, x='month', y='value', order=month_order,ax=ax2)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
