import pandas as pd
from typing import Dict, Any, Tuple

def clean_data(df: pd.DataFrame, mapping: Dict[str, str]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    df_clean = df.copy()
    report = {
        'initial_rows': len(df_clean), 'duplicates_removed': 0, 'missing_values_handled': 0,
        'invalid_dates': 0, 'invalid_numerics': 0, 'final_rows': 0, 'quality_score': 0.0,
        'rating': 'Poor', 'commentary': []
    }

    reverse_mapping = {v: k for k, v in mapping.items() if v is not None}
    df_clean = df_clean.rename(columns=reverse_mapping)

    # 1. Deduplicate
    initial_len = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    report['duplicates_removed'] = initial_len - len(df_clean)

    # 2. Date Handling
    if 'Date' in df_clean.columns:
        df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce')
        report['invalid_dates'] = int(df_clean['Date'].isna().sum())
        df_clean = df_clean.dropna(subset=['Date'])

    # 3. Numeric Handling
    for col in ['Revenue', 'Quantity']:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            report['invalid_numerics'] += int(df_clean[col].isna().sum())
            df_clean[col] = df_clean[col].fillna(0 if col == 'Quantity' else df_clean[col].median())

    # 4. Categorical Handling
    for col in ['Product', 'Category', 'Customer', 'Region', 'Salesperson', 'Order_ID']:
        if col in df_clean.columns:
            missing = df_clean[col].isna().sum()
            report['missing_values_handled'] += int(missing)
            df_clean[col] = df_clean[col].fillna('Unknown')

    report['final_rows'] = len(df_clean)
    
    # Quality Score Calculation
    completeness = (report['final_rows'] / report['initial_rows']) * 100 if report['initial_rows'] > 0 else 100
    duplicate_rate = (report['duplicates_removed'] / report['initial_rows']) * 100 if report['initial_rows'] > 0 else 0
    score = completeness - (duplicate_rate * 2) - (report['invalid_dates'] / report['initial_rows'] * 100 if report['initial_rows'] > 0 else 0)
    report['quality_score'] = max(0, min(100, round(score, 1)))

    if report['quality_score'] >= 90:
        report['rating'], msg = 'Excellent', "Dataset quality is excellent. Data is highly reliable for forecasting."
    elif report['quality_score'] >= 75:
        report['rating'], msg = 'Good', "Dataset quality is good. Minor data cleaning was applied successfully."
    elif report['quality_score'] >= 50:
        report['rating'], msg = 'Moderate', "Dataset quality is moderate. Interpret with caution due to missing data."
    else:
        report['rating'], msg = 'Poor', "Dataset quality is poor. Significant data issues detected."
    
    report['commentary'].append(msg)
    if report['duplicates_removed'] > 0:
        report['commentary'].append(f"Removed {report['duplicates_removed']} duplicate transactions.")
    
    return df_clean, report