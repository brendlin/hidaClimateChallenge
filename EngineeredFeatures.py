
def getGlobalTemperatureAverageSeries(temperatureSeries) :
    # Input is the temperature series, e.g. data['T2m']
    # Output is the average global temperature for each year.
    spatial_averaged = temperatureSeries.groupby('time').mean()
    return spatial_averaged
    
def getTemporalAveragedForAnomaly(temperatureSeries) :
    # Input is the temperature series, e.g. data['T2m']
    # Output is average temperatuers at each latitude and longitude
    temporal_averaged = temperatureSeries.groupby(['lat','lon']).mean()
    return temporal_averaged

def getRollingAverage(series,window=11,center=True) :
    rolling = series.rolling(window=window,center=center).mean()
    return rolling
