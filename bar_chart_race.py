# Import Pandas for data base manipulation
# Import dataprocessing - the processed original data script/database.
# Import matplotlib to make plot and animated data
import pandas as pd
import data_processing as dp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Creating the database and popping all unused values, to clean the database
# and ready it for formattig.
infectData = dp.create_database()
infectData.pop("areaCode")
infectData.pop("newCasesBySpecimenDateChange")
infectData.pop("newCasesBySpecimenDateChangePercentage")
infectData.pop("newCasesBySpecimenDateDirection")
infectData.pop("newCasesBySpecimenDateRollingSum")
infectData.sort_index()

# Uses the to_datetime function to create an ordered date sequence for the
# values to plot appropriately
infectData["date"] = pd.to_datetime(infectData["date"], dayfirst=True)
infectData.sort_values(by="date")

# groupData is a formatted database, reindexing the values from infectData
# and turning it into a wide-date table so it can be turned into a bcr.
groupData = infectData.pivot_table(values="newCasesBySpecimenDateRollingRate"
                                   , index="date", columns="areaName")


# Fills all NaN values with 0 and sorts the index of groupData.
groupData.fillna(0, inplace=True)
df = groupData.sort_index()

# Locates the positions based on length in groupData and counts the
# cumulative sum and updates the database respectively.
df.iloc[:, 0:-1] = groupData.iloc[:, 0:-1].cumsum()

# This function sorts and sets the axes
def setAxes(ax):
    # ax.set_facecolor('.8')
    ax.tick_params(labelsize=10, length=0)
    # Disables Gridline
    ax.grid(True, axis='x', color='white')
    # Set axis below
    ax.set_axisbelow(True)
    [spine.set_visible(True) for spine in ax.spines.values()]
   


# Getting data ready to plot
def ready_data(df):
    df = df.reset_index()

    last_idx = df.index[-1] + 1
    ready_width = df.reindex(range(last_idx))
    ready_width['date'] = ready_width['date'].fillna(method='ffill')
    ready_width = ready_width.set_index('date')
    # Setting a colour for each place
    ready_y = ready_width.rank(axis=1, method='first')
    return ready_width, ready_y

ready_width, ready_y = ready_data(df)


labels = ready_width.columns
colors = plt.cm.Dark2(range(6))


def update(i):
    ax.clear()
    for line in ax.containers:
        line.remove()
    y = ready_y.iloc[i]
    width = ready_width.iloc[i]
    # Plotting bar graph
    ax.barh(y=y, width=width, color=colors, tick_label=labels)
    #Plotting the title and date
    date_str = ready_width.index[i].strftime('%d-%m-%Y')
    ax.set_title(f'Covid Cases in Bristol by Date (Rolling Rate) - {date_str}', fontsize='smaller')
    ax.set_ylim(44.5,54.5)
    return ax
  
# Setting the figure size
fig = plt.figure(figsize=(17, 6))
ax = fig.add_subplot(1, 1, 1)

def genBarChart():
    print('Your gif is now being created, please wait...')
    anim = FuncAnimation(fig=fig, func=update, frames=len(ready_width), 
                    interval=200, repeat=False)


    anim.save("bar_chart.gif")
    print('Saved as bar_chart.gif')

