import pandas as pd
import numpy as np
from typing import Dict, Any

def forecast_sales(df: pd.DataFrame, periods: int = 3) -> Dict[str, Any]:
    df['Date'] = pd.to_datetime(df['Date'])
    monthly_rev = df.groupby(df['Date'].dt.to_period('M'))['Revenue'].sum().reset_index()
    monthly_rev['Date'] = monthly_rev['Date'].dt.to_timestamp().sort_values()
    
    values = monthly_rev['Revenue'].values
    dates = monthly_rev['Date'].values
    weights = np.array([0.5, 0.3, 0.2]) # WMA weights
    forecasts, last_dates = [], pd.to_datetime(dates[-3:])
    
    for i in range(periods):
        wma = np.sum(values[-3:] * weights) if len(values) >= 3 else np.mean(values)
        trend = (values[-1] - values[-2]) / values[-2] if len(values) >= 2 else 0
        wma = wma * (1 + trend)
        forecasts.append(wma)
        values = np.append(values, wma)
        last_dates = np.append(last_dates, last_dates[-1] + pd.DateOffset(months=1))

    std_dev = np.std(values[-6:]) if len(values) >= 6 else np.std(values)
    
    forecast_df = pd.DataFrame({
        'Date': pd.to_datetime(last_dates[-periods:]),
        'Forecast': forecasts,
        'Lower_Bound': [max(0, f - 1.5 * std_dev) for f in forecasts],
        'Upper_Bound': [f + 1.5 * std_dev for f in forecasts]
    })
    return {'forecast_df': forecast_df, 'method': 'Weighted Moving Average with Trend Adjustment'}