# Corona Plot

This code is inteded to be run every day (e.g. with
cron) and creates a plot of the total COVID-19 cases in Italy versus
time. The data is downloaded from [the official git
repository](https://github.com/pcm-dpc/COVID-19) and fitted by two
sigmoid functions to try to predict the overall behaviour.

## Classes

### Class CoronaData

The class `CoronaData` creates the dataframe with the data to be
plotted. The method `from_git_italy` downloads the data from the
 git repository of the italian government. Alternatively, the data can
 be loaded directly from a file with the method `from_file`.

### Class CoronaPlot

The class CoronaPlot takes the data and plots it with matplotlib. The fit with two
sigmoids representing the two infection waves is also done within this
class. Note that for the fit to work, the discrete time data in date
format is transformed into seconds format. The plot is saved as a
png-file. The user can choose where it should be saved. 
