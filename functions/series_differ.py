def differ(series):

  from statsmodels.tsa.stattools import adfuller

  while adfuller(series)[1] > 0.15:
    series = series.diff().dropna()

  return series