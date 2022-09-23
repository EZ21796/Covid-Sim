# FCP Assignment: Graphical Analysis & Simulation of Covid-19

## Requirements

Use the package manager conda in the conda prompt to install all additional packages required:

* numpy
```
pip install numpy
```

* pandas
```
pip install pandas
```

* matplotlib
```
pip install matplotlib
```

* geopandas
    * If you have issues with the command below please refer to the packages documentation at https://geopandas.org/en/stable/getting_started/install.html. This can take up to 30mins in some cases so please be patient.
```
conda install geopandas
```

* descartes
```
pip install descartes
```

## How to run
The code must be run from anaconda prompt

1. Navigate to the github repos local directory
2. You can select which part of the code you want to run by using these arguments:  

* To open the GUI
```
$ python main.py -UI
# The UI can sometimes freeze when generating plots. This is normal please wait for the UI to start responding again. You can see updates of when the figure is complete in the command line
```

* To create the choropleth map
```
$ python main.py -map
``` 

* To create the bar chart race
```
$ python main.py -bar
``` 

* To run the sim with default values
```
$ python main.py -sim
``` 

The sim can be run with customized using 3 different arguments. These can be run in any combination. Each argument must be followed by an integer between 0 and 100.
```
#chance of contracting the virus upon contact
$ python main.py -sim -con {integer between 1-100} 
```
```
#chance a person recovers from the virus, lower values increases recovery time
$ python main.py -sim -rec {integer between 1-100} 
```
```
#chance a person dies due to virus
$ python main.py -sim -dead {integer between 1-100}
``` 
