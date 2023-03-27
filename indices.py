"""This script includes functions that define the various extreme variables we will by deriving"""

import numpy as np
import xclim.indices as xci
from xclim.core.calendar import percentile_doy
from xclim.core.units import convert_units_to, to_agg_units
from xclim.indices.generic import threshold_count


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
    """'Hot Day' - the 6th hottest day of the year
    
    Args:
        tasmax (xarray.DataArray): daily maximum temperature values for a year
        
    Returns:
        Hot Day values for each year
    """
    def func(tasmax):
        # np.sort defaults to ascending.. 
        #   hd is simply "6th hottest" day
        return tasmax.reduce(take_sorted, dim="time", idx=-6)
    
    # hardcoded unit conversion
    out = tasmax.resample(time="1Y").map(func) - 273.15
    out.attrs["units"] = "C"
    out.attrs["comment"] = "'hot day': 6th hottest day of the year"
    
    return out
    

def cd(tasmin):
    """'Cold Day' - the 6th coldest day of the year
    
    Args:
        tasmin (xarray.DataArray): daily minimum temperature values
        
    Returns:
        Cold Day values for each year
    """
    def func(tasmin):
        # time_ax = np.where(np.array(tasmin.dims) == "time")[0][0]
        # np.sort defaults to ascending.. 
        #   cd is simply "6th coldest" day
        return tasmin.reduce(take_sorted, dim="time", idx=5)
    
    # hardcoded unit conversion
    out = tasmin.resample(time="1Y").map(func) - 273.15
    out.attrs["units"] = "C"
    out.attrs["comment"] = "'cold day': 6th coldest day of the year"
    
    return out


def hsd(prsn):
    """'Heavy snow days' - the mean snowfall of the 5 snowiest days in a year
    
    Args:
        prsn (xarray.DataArray): daily total snowfall values
        
    Returns:
        The mean snowfall for the 5 snowiest days in a year
    """
    def func(prsn):
        def take_sorted_mean(arr, axis, idx):
            """Wrapper for take_sorted function to give the mean of the taken values"""
            return take_sorted(arr, axis, idx).mean(axis=axis)
        
        return prsn.reduce(take_sorted_mean, dim="time", idx=np.arange(-5, 0))
    
    out = prsn.resample(time="1Y").map(func) * 8640
    out.attrs["units"] = "cm"

    return out
    

def rx1day(pr):
    """'Max 1-day precip' - the max daily precip value recorded for a year.
    
    Args:
        pr (xarray.DataArray): daily total precip values
        
    Returns:
        Max 1-day precip for each year
    """
    out = xci.max_n_day_precipitation_amount(pr, freq="YS")
    out.attrs["units"] = "mm"
    
    return out


def rx5day(pr):
    """'Max 5-day precip' - the max 5-day precip value recorded for a year.
    
    Args:
        pr (xarray.DataArray): daily total precip values
        
    Returns:
        Max 5-day precip for each year
    """
    out = xci.max_n_day_precipitation_amount(pr, 5, freq="YS")
    out.attrs["units"] = "mm"
    
    return out


def su(tasmax):
    """'Summer days' - the number of days with tasmax above 25 C
    
    Args:
        tasmax (xarray.DataArray): daily maximum temperature values for a year
        
    Returns:
        Number of summer days for each year
    """
    return xci.tx_days_above(tasmax, "25 degC", freq="YS")


def dw(tasmin):
    """'Deep winter days' - the number of days with tasmin below -30 C
    
    Args:
        tasmin (xarray.DataArray): daily maximum temperature values for a year
        
    Returns:
        Number of deep winter days for each year
    """
    return xci.tn_days_below(tasmin, thresh="-30 degC", freq="YS")


def wsdi(tasmax, hist_da):
    """'Warm spell duration index' - Annual count of occurrences of at least 5 consecutive days with daily max T above 90th percentile of historical values for the date
    
    Args:
        tasmax (xarray.DataArray): daily maximum temperature values
        hist_da (xarray.DataArray): historical daily maximum temperature values
        
    Returns:
        Warm spell duration index for each year
    """
    tasmax_per = percentile_doy(hist_da, per=90).sel(percentiles=90)
    return xci.warm_spell_duration_index(tasmax, tasmax_per, window=6, freq="YS").drop("percentiles")


def csdi(tasmin, hist_da):
    """'Cold spell duration index' - Annual count of occurrences of at least 5 consecutive days with daily min T below 10th percentile of historical values for the date
    
    Args:
        tasmin (xarray.DataArray): daily minimum temperature values for a year
        hist_da (xarray.DataArray): historical daily minimum temperature values
        
    Returns:
        Cold spell duration index for each year
    """
    tasmin_per = percentile_doy(hist_da, per=10).sel(percentiles=10)
    return xci.cold_spell_duration_index(tasmin, tasmin_per, window=6, freq="YS").drop("percentiles")


def r10mm(pr):
    """'Heavy precip days' - number of days in a year with over 10mm of precip
    
    Args:
        pr (xarray.DataArray): daily total precip values
        
    Returns:
        Number of heavy precip days for each year
    """
    # code based on xclim.indices._threshold.tg_days_above
    thresh = "10 mm/day"
    thresh = convert_units_to(thresh, pr)
    f = threshold_count(pr, ">", thresh, freq="YS")
    return to_agg_units(f, pr, "count")


def cwd(pr):
    """'Consecutive wet days' - number of the most consecutive days with precip > 1 mm
    
    Args:
        pr (xarray.DataArray): daily total precip values
        
    Returns:
        Max number of consecutive wet days for each year
    """
    return xci.maximum_consecutive_wet_days(pr, thresh=f"1 mm/day", freq="YS")


def cdd(pr):
    """'Consecutive dry days' - number of the most consecutive days with precip < 1 mm
    
    Args:
        pr (xarray.DataArray): daily total precip values
        
    Returns:
        Max number of consecutive dry days for each year
    """
    return xci.maximum_consecutive_dry_days(pr, thresh=f"1 mm/day", freq="YS")


def wndd(sfcWind):
    """'Windy days' - number of days with mean wind speed > 10 m/s
    
    Args:
        sfcWind (xarray.DataArray): Daily average near-surface wind speed 
        
    Returns:
        Max number of consecutive windy days for each year
    """
    # code based on xclim.indices._threshold.tg_days_above
    thresh = "10 m s-1"
    thresh = convert_units_to(thresh, sfcWind)
    f = threshold_count(sfcWind, ">", thresh, freq="YS")
    return to_agg_units(f, sfcWind, "count")


def compute_index(da, index, model, scenario, kwargs={}):
    """Summarize a DataArray according to a specified index / aggregation function
    
    Args:
        da (xarray.DataArray): the DataArray object containing the base variable data to b summarized according to aggr
        index (str): String corresponding to the name of the index to compute (assumes value is equal to the name of the corresponding function)
        scenario (str): scenario being run (for new coordinate dimension)
        model (str): model being run (for new coordinate dimension)
        kwargs (dict): additional arguments for the index function being called
            
    Returns:
        A new data array with dimensions year, latitude, longitude, in that order containing the summarized information
    """
    new_da = (
        globals()[index](da, **kwargs)
        .transpose("time", "lat", "lon")
        .reset_coords(["longitude", "latitude", "height"], drop=True)
    )
    new_da.name = index  
    # get the nodata mask from first time slice
    nodata = np.broadcast_to(
        np.isnan(da.sel(time=da["time"].values[0]).transpose("lat", "lon")), 
        new_da.shape
    )
    # remask, because xclim switches nans to 0
    # xclim is inconsistent about the types returned.
    if new_da.dtype in [np.int32, np.int64]:
        new_da.values[nodata] = -9999
    else:
        new_da.values[nodata] = np.nan
    
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
