
import pandas as pd
import numpy as np
import pandas_flavor as pf

from dateutil import parser
from warnings import warn



@pf.register_series_method
def floor_date(
    idx: pd.Series or pd.DatetimeIndex, 
    unit: str = "D",
) -> pd.Series:
    '''Round a date down to the specified unit (e.g. Flooring).
    
    The `floor_date` function takes a pandas Series of dates and returns a new Series with the dates rounded down to the specified unit.
    
    Parameters
    ----------
    idx : pd.Series or pd.DatetimeIndex
        The `idx` parameter is a pandas Series or pandas DatetimeIndex object that contains datetime values. It represents the dates that you want to round down.
    unit : str, optional
        The `unit` parameter in the `floor_date` function is a string that specifies the time unit to which the dates in the `idx` series should be rounded down. It has a default value of "D", which stands for day. Other possible values for the `unit` parameter could be
    
    Returns
    -------
    pd.Series 
        The `floor_date` function returns a pandas Series object containing datetime64[ns] values.
    
    Examples
    --------
    ```{python}
    import timetk as tk
    import pandas as pd
    
    dates = pd.date_range("2020-01-01", "2020-01-10", freq="1H")
    dates
    ```
    
    ```{python}
    # Works on DateTimeIndex
    tk.floor_date(dates, unit="D")
    ```
    
    ```{python}
    # Works on Pandas Series
    dates.to_series().floor_date(unit="D")
    ```
    '''
    
    # If idx is a DatetimeIndex, convert to Series
    if isinstance(idx, pd.DatetimeIndex):
        idx = pd.Series(idx, name="idx")
    
    # Check if idx is a Series
    if not isinstance(idx, pd.Series):
        raise TypeError('idx must be a pandas Series or DatetimeIndex object')
    
    # Convert to period
    period = idx.dt.to_period(unit)

    try:
        date = period.dt.to_timestamp()
    except:
        warn("Failed attempt to convert to pandas timestamp. Returning pandas period instead.")
        date = period

    return date

@pf.register_series_method
def week_of_month(idx: pd.Series or pd.DatetimeIndex,) -> pd.Series:
    '''The "week_of_month" function calculates the week number of a given date within its month.
    
    Parameters
    ----------
    idx : pd.Series or pd.DatetimeIndex
        The parameter "idx" is a pandas Series object that represents a specific date for which you want to determine the week of the month.
    
    Returns
    -------
    pd.Series
        The week of the month for a given date.
    
    Examples
    --------
    ```{python}
    import timetk as tk
    import pandas as pd
    
    dates = pd.date_range("2020-01-01", "2020-02-28", freq="1D")
    dates
    ```
    
    ```{python}
    # Works on DateTimeIndex
    tk.week_of_month(dates)
    ```
    
    ```{python}
    # Works on Pandas Series
    dates.to_series().week_of_month()
    ```
    
    '''
    
    if isinstance(idx, pd.DatetimeIndex):
        idx = pd.Series(idx, name="idx")
    
    if not isinstance(idx, pd.Series):
        raise TypeError('idx must be a pandas Series or DatetimeIndex object')
    
    ret = (idx.dt.day - 1) // 7 + 1
    
    ret = pd.Series(
        ret, 
        name="week_of_month", 
        index = idx.index
    )
    
    return ret




def is_datetime_string(x: str or pd.Series or pd.DatetimeIndex) -> bool:
    
    if isinstance(x, pd.Series):
        x = x.values[0]
    
    if isinstance(x, pd.DatetimeIndex):
        x = x[0]
    
    try:
        parser.parse(str(x))
        return True
    except ValueError:
        return False
    
def detect_timeseries_columns(data: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
    
    df = data.head(1)
    
    if verbose:
        print(df)
    
    return df.map(is_datetime_string)

def has_timeseries_columns(data: pd.DataFrame, verbose: bool = False) -> bool:
    
    if verbose:
        print(detect_timeseries_columns(data).iloc[0])
    
    return detect_timeseries_columns(data).iloc[0].any()

def get_timeseries_colname(data: pd.DataFrame, verbose: bool = False) -> str:
    
    if verbose:
        print(detect_timeseries_columns(data).iloc[0])
        
    return detect_timeseries_columns(data).iloc[0].idxmax()

@pf.register_series_method
def get_pandas_frequency(idx: pd.Series or pd.DatetimeIndex, force_regular: bool = False) -> str:
    '''
    Get the frequency of a pandas Series or DatetimeIndex.
    
    The function `get_pandas_frequency` takes a Pandas Series or DatetimeIndex as input and returns the inferred frequency of the index, with an option to force regular frequency.
    
    Parameters
    ----------
    idx : pd.Series or pd.DatetimeIndex
        The `idx` parameter can be either a `pd.Series` or a `pd.DatetimeIndex`. It represents the index or the time series data for which we want to determine the frequency.
    force_regular : bool, optional
        The `force_regular` parameter is a boolean flag that determines whether to force the frequency to be regular. If set to `True`, the function will convert irregular frequencies to their regular counterparts. For example, if the inferred frequency is 'B' (business days), it will be converted to 'D' (calendar days). The default value is `False`.
    
    Returns
    -------
    str
        The frequency of the given pandas series or datetime index.
    
    '''
   
    
    if isinstance(idx, pd.Series):
        idx = idx.values
        
    _len = len(idx)
    if _len > 10:
        _len = 10
    
    dt_index = pd.DatetimeIndex(idx[0:_len])
    
    freq = dt_index.inferred_freq
    
    if freq is None:
            raise ValueError("The frequency could not be detectied.")
    
    if force_regular:
        if freq == 'B':
            freq = 'D'
        if freq == 'BM':
            freq = 'M'
        if freq == 'BQ':
            freq = 'Q'
        if freq == 'BA':
            freq = 'A'
        if freq == 'BY':
            freq = 'Y'
        if freq == 'BMS':
            freq = 'MS'
        if freq == 'BQS':
            freq = 'QS'
        if freq == 'BYS':
            freq = 'YS'
        if freq == 'BAS':
            freq = 'AS'
        
    
    return freq

