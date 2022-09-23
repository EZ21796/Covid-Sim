import pandas as pd
import geopandas as gpd
import data_processing as dp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import make_axes_locatable

def geodf_create():
    msoa_bristol = gpd.read_file(r'data/bristol_msoa11_map_data/msoa11.shp')
    
    msoa_bristol.pop('lacd')
    msoa_bristol.pop('area_m2')
    msoa_bristol.pop('perimeter_m')
    msoa_bristol.pop('mi_prinx')
    msoa_bristol.pop('objectid')
    msoa_bristol.pop('msoa11nm')
    
    msoa11cd_end = []
    for msoa11cd in msoa_bristol['msoa11cd'].values:
        msoa11cd_end.append(msoa11cd[-4:])
    
    msoa_bristol['msoa11cd_end'] = msoa11cd_end
    msoa_cases_ordered = msoa_bristol.sort_values(by=['msoa11cd_end'])
    msoa_cases_ordered.pop('msoa11cd_end')
    msoa_cases_ordered = msoa_cases_ordered.rename(columns = {'msoa11cd':'areaCodes'})
    
    covid_data = dp.create_database()
    
    covid_data.pop('areaName')
    covid_data.pop('newCasesBySpecimenDateChange')
    covid_data.pop('newCasesBySpecimenDateChangePercentage')
    covid_data.pop('newCasesBySpecimenDateDirection')
    covid_data.pop('newCasesBySpecimenDateRollingRate')
    
    #makes list of each unique date that a reading has been taken
    unique_dates = []
    for date in covid_data['date']:
        if date not in unique_dates:
            unique_dates.append(date)
    unique_dates.reverse()
    
    unique_area_codes = []
    for area_code in covid_data['areaCode']:
        if area_code not in unique_area_codes:
            unique_area_codes.append(area_code)
    
    
    unique_data = {'areaCodes': unique_area_codes}
    
    cases_columns = pd.DataFrame(unique_data)
    
    cases_columns_index_list= cases_columns.index.tolist()
    
    areacode_index_dict = dict(zip(unique_area_codes, cases_columns_index_list))
    
    for date in unique_dates:
        index_count = 0
        for covid_data_date in covid_data['date'].values:
            if date == covid_data_date:
                
                current_area_code = covid_data.at[index_count, 'areaCode']
                cases_columns_index = areacode_index_dict[current_area_code]
                cases_columns.at[cases_columns_index, date] = covid_data.at[index_count, 'newCasesBySpecimenDateRollingSum']
            cases_columns = cases_columns.copy()
            index_count += 1
    
    cases_columns = cases_columns.fillna(0)
        
    msoa_cases_ordered = msoa_cases_ordered.merge(cases_columns)
    
    return msoa_cases_ordered, unique_dates


def plot_animation(geo_df, dates):
    vmin, vmax = 0, 350
    color_map = 'Reds'
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)

    def animate(i):
        ax.clear()
        geo_df.plot(column = dates[i], cmap = color_map, ax=ax, figsize=(10,10), linewidth=0.6, edgecolor = 'black', vmin=vmin, vmax=vmax, legend=True, cax=cax)
        ax.set_title(f'Number of new cases in week beginning {dates[i]}', fontdict={'fontsize': '15', 'fontweight' : '3'})
        ax.set_axis_off()
        

    ani = FuncAnimation(fig, animate, interval=200, repeat=False, blit=False)
    
    plt.close()
    ani.save('bristol_covid_map.gif', dpi=300)

fig, ax = plt.subplots(1, 1)

def create_choropleth():
    print('Creating choropleth map')
    geodf, dates = geodf_create()
    ani = plot_animation(geodf, dates)
    print('Saved as bristol_covid_map.gif')

#create_choropleth()