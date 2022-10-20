"""This script includes functions that define the various extreme variables we will by deriving"""

import numpy as np
import xclim.indices as xi


def take_sorted(arr, axis, idx):
    """Helper function for the 'hot day' and 'cold day' indices to slice a numpy array after sorting it. Done in favor of fixed, []-based indexing.
    
    Args:
        arr (numpy.ndarray): array
        axis (int): axis to sort and slice according to
        idx (int): index value to slice arr at across all other axes
        
    Returns:
        array of values at position idx of arr sorted along axis
    """
    return np.take(np.sort(arr, axis), idx, axis)


def hd(tasmax):
    """'Hot Day' - the 6th hottest day of the year, over axis called "time"
    
    Args:
        tasmax (xarray.DataArray): daily maximum temperature values for a year
        
    Returns:
        Hot Day values for each year
    """
    def func(tasmax):
        time_ax = np.where(np.array(tasmax.dims) == "time")[0][0]
        # np.sort defaults to ascending.. 
        #   hd is simply "6th hottest" day
        return tasmax.reduce(take_sorted, dim="time", idx=-6)
    
    return tasmax.resample(time="1Y").map(func)
    

def cd(tasmin):
    """'Cold Day' - the 6th coldest day of the year, over axis called "time"
    
    Args:
        tasmin (xarray.DataArray): daily minimum temperature values
        
    Returns:
        Cold Day values for each year
    """
    def func(tasmin):
        time_ax = np.where(np.array(tasmin.dims) == "time")[0][0]
        # np.sort defaults to ascending.. 
        #   cd is simply "6th coldest" day
        return tasmin.reduce(take_sorted, dim="time", idx=5)
    
    return tasmin.resample(time="1Y").map(func)


def rx1day(pr):
    """'Max 1-day precip' - the max daily precip value recorded for a year.
    
    Args:
        pr (xarray.DataArray): daily total precip values
        
    Returns:
        Max 1-day precip for each year
    """
    return xi.max_n_day_precipitation_amount(pr, freq="YS")
    

def hsd(prsn):
    """'Heavy snow days' - number of days in a year with over 10cm of snowfall
    
    Args:
        prsn (xarray.DataArray): daily total snowfall values
        
    Returns:
        Number of heavy snow days for each year
    """
    # convert 10cm to native units of prsn files, kg m-2 s-1
    hsd_thr = 10 / 8640
    return xi.days_with_snow(prsn, low=f"{hsd_thr} kg m-2 s-1", freq="YS")


def rx5day(pr):
    """'Max 5-day precip' - the max 5-day precip value recorded for a year.
    
    Args:
        pr (xarray.DataArray): daily total precip values
        
    Returns:
        Max 5-day precip for each year
    """
    return xi.max_n_day_precipitation_amount(pr, 5, freq="YS")


def su(tasmax):
    """'Summer days' - the number of days with tasmax above 25 C
    
    Args:
        tasmax (xarray.DataArray): daily maximum temperature values for a year
        
    Returns:
        Number of summer days for each year
    """
    return xi.tx_days_above(tasmax, "25 degC", freq="YS")


def dw(tasmin):
    """'Deep winter days' - the number of days with tasmin below -30 C
    
    Args:
        tasmin (xarray.DataArray): daily maximum temperature values for a year
        
    Returns:
        Number of deep winter days for each year
    """
    return xi.tn_days_below(tasmin, thresh="-30 degC", freq="YS")


# def wsdi(tas):
#     """'Warm spell duration index' - Annual count of occurrences of at least 5 consecutive days with daily mean T above 90 th percentile of historical values for the date
    
#     Args:
#         tas (xarray.DataArray): daily mean temperature values for a year
        
#     Returns:
#         Warms spell duration index for each year
#     """
#     return xi


def r10mm(pr):
    """'Heavy precip days' - number of days in a year with over 10mm of precip
    
    Args:
        pr (xarray.DataArray): daily total precip values
        
    Returns:
        Number of heavy precip days for each year
    """
    return xi.days_over_precip_thresh(pr, thresh=f"10 mm/day", freq="YS")


def cwd(pr):
    """'Consecutive wet days' - number of the most consecutive days with precip > 1 mm
    
    Args:
        pr (xarray.DataArray): daily total precip values
        
    Returns:
        Max number of consecutive wet days for each year
    """
    return xi.maximum_consecutive_wet_days(pr, thresh=f"1 mm/day", freq="YS")


def cdd(pr):
    """'Consecutive dry days' - number of the most consecutive days with precip < 1 mm
    
    Args:
        pr (xarray.DataArray): daily total precip values
        
    Returns:
        Max number of consecutive dry days for each year
    """
    return xi.maximum_consecutive_dry_days(pr, thresh=f"1 mm/day", freq="YS")


def wndd(pr):
    """'Consecutive windy days' - number of the most consecutive days with mean wind speed > 10 m/s
    
    Args:
        sfcWind (xarray.DataArray): Daily average near-surface wind speed 
        
    Returns:
        Max number of consecutive windy days for each year
    """
    return xi.maximum_consecutive_dry_days(pr, thresh=f"10 m s-1", freq="YS")


def compute_index(da, index, model, scenario):
    """Summarize a DataArray according to a specified index / aggregation function
    
    Args:
        da (xarray.DataArray): the DataArray object containing the base variable data to b summarized according to aggr
        index (str): String corresponding to the name of the index to compute
        scenario (str): scenario being run (for new coordinate dimension)
        model (str): model being run (for new coordinate dimension)
            
    Returns:
        A new data array with dimensions year, latitude, longitude, in that order containing the summarized information
    """
    new_da = (
        aggr_func_lu[index](da)
        .transpose("time", "lat", "lon")
        .reset_coords(["longitude", "latitude", "height"], drop=True)
    )
    new_da.name = index
    
    # add model and scenario coordinate dimensions to the data array
    coords_di = {
        "model": model,
        "scenario": scenario,
    }

    new_dims = list(coords_di.keys())
    new_da = new_da.assign_coords(coords_di).expand_dims(new_dims)
    # convert the time dimension to integer years instead of CF time objects
    years = [cftime.year for cftime in new_da.time.values]
    new_da = new_da.rename({"time": "year"}).assign_coords({"year": years})
    
    return new_da


aggr_func_lu = {
    "hd": hd,
    "cd": cd,
    "rx1day": rx1day,
    "hsd": hsd,
}
