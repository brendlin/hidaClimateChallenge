
def getTimeSlice(temperatureSeries,time_yr) :
    # This is very easy... just add 716 (bizarrely) to the time * 10000
    if time_yr < 1 or time_yr > 999 :
        print('Error - out of range')
        raise ValueError
    return temperatureSeries.xs(time_yr*10000 + 716.0, level='time')


def Unstack(timeSlice) :
    # (For use with the temperatureSeries)
    # Unstack a time slice (turn into pandas dataframe)
    # Rows are latitude, columns are longitude

    unstacked = timeSlice.unstack(fill_value=0)

    # Renaming 180-360 to -180-0.
    # Also adding a tiny offset.
    rename_to = dict()
    for c in unstacked.columns :
        rename_to[c] = (c-180)%360-180+15/16
    unstacked = unstacked.rename(columns=rename_to)

    # Sort the columns from -180 to +180
    columns = unstacked.columns.to_list()
    columns.sort()
    unstacked = unstacked[columns]
    return unstacked


def plotMap(timeSlice,fig,ax,vmin=None,vmax=None,add_colorbar=True) :
    # (For use with the temperatureSeries)
    # Plot the map, given a timeSlice.
    # Takes the output of getTimeSlice
    # (e.g. a series consisting of lat and lon multiindex values)

    import numpy as np
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs

    unstacked = Unstack(timeSlice)

    cm = plt.get_cmap('cividis')
    levels = None

    # If you do not set levels, then you do not have control over the min/max
    # of the colorbar !!!
    if vmin != None and vmax != None :
        levels = np.linspace(vmin, vmax, 20+1)

    # Make the mesh grid
    lon = unstacked.columns
    lat = unstacked.index
    m_lon, m_lat = np.meshgrid(lon, lat)

    the_contour = ax.contourf(m_lon, m_lat,unstacked.values,transform=ccrs.PlateCarree(),
                              cmap=cm,levels=levels,vmin=vmin,vmax=vmax)
    the_contour.set_clim(vmin,vmax)
    ax.set_global()
    ax.coastlines()
    if add_colorbar :
        fig.colorbar(the_contour,ax=[ax])
    return the_contour


def plotTimeSlice(temperatureSeries,time_yr,fig,ax,vmin=None,vmax=None) :
    # (For use with the temperatureSeries)
    # Same as plotMap, but you simply have to give the year (integer)

    # get the slice
    slicex = getTimeSlice(temperatureSeries,time_yr)

    ax.title.set_text('Year %s'%(time_yr))
    return plotMap(slicex,fig,ax,vmin,vmax)


def getLatSlice(temperatureSeries,lower,upper) :
    # Get a specific latitude slice
    #
    all_lat = temperatureSeries.index.get_level_values('lat')
    allowed = []
    for lati in all_lat :
        if lati > upper :
            continue
        if lati < lower :
            continue
        allowed.append(lati)
    return temperatureSeries.loc[temperatureSeries.index.isin(list(allowed), level='lat')]


def getSolarForcingData(filename) :
    # Returns a pandas dataframe for the solar forcing data

    import xarray as xr
    import numpy as np

    ds = xr.open_dataset(filename)
    TSI = ds.to_dataframe()['TSI']

    # "lev" and "x" seem to be meaningless, so let's get rid of them and turn the series into a dataframe.
    TSI = TSI.xs((1.0)).xs(0,level='x').to_frame()
    TSI = TSI.reset_index()

    # Make a "time_yr" column
    TSI['time_yr'] = np.round(TSI['time']/10000)

    return TSI
