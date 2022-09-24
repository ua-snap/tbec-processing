"""This script includes functions that define the various extreme variables we will by deriving"""

import numpy as np
from xclim.indices import max_1day_precipitation_amount
from xclim.indices import days_with_snow


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


# keeping this for now in case we end up adding more indices that aren't defined in xclim
# def wrap_resample_map(da, func):
#     """Wrapper for mapping function to grouped dataarray"""
#     da.resample(time="1Y").map(func)


def hd(tasmax):
    """'Hot Day' - the 6th hottest day of the year, over axis called "time"
    
    Args:
        tasmax (xarray.DataArray): daily maximum temperature values for a year
        
    Returns:
        Hot Day computed over the "time" dimension
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
        Cold Day computed over the "time" dimension
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
        Max 1-day precip computed over the time dimension
    """
    return max_1day_precipitation_amount(pr,  freq="YS")
    

def hsd(prsn):
    """'Heavy snow days' - number of days in a year with over 10cm of snowfall
    
    Args:
        prsn (xarray.DataArray): daily total snowfall values
        
    Returns:
        Number of heavy snow days computed over time dimension
    """
    # convert 10cm to native units of prsn files, kg m-2 s-1
    hsd_thr = 10 / 8640
    return days_with_snow(ds["prsn"], low=f"{hsd_thr} kg m-2 s-1", freq="YS")


aggr_func_lu = {
    "hd": hd,
    "cd": cd,
    "rx1day": rx1day,
    "hsd": hsd,
}