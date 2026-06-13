from fuzzywuzzy import process
from typing import Dict, Tuple

ALIAS_DICT = {
    'Date': ['date', 'order date', 'transaction date', 'time', 'day'],
    'Revenue': [
    'revenue',
    'total revenue',
    'sales',
    'sales amount',
    'sales value',
    'gross sales',
    'net sales',
    'amount',
    'revenue amount',
    'revenue inr',
    'turnover',
    'income',
    'value'
],
    'Quantity': ['quantity', 'qty', 'units', 'volume'],
    'Product': ['product', 'item', 'sku', 'product name', 'item name'],
    'Category': ['category', 'product category', 'segment', 'class'],
    'Customer': ['customer', 'client', 'customer name', 'account', 'buyer'],
    'Region': ['region', 'territory', 'zone', 'area', 'country', 'state'],
    'Salesperson': ['salesperson', 'sales rep', 'rep', 'employee', 'agent'],
    'Order_ID': ['order id', 'order_id', 'transaction id', 'invoice', 'receipt']
}

REQUIRED_COLUMNS = ['Date', 'Revenue']

def map_columns(df: pd.DataFrame) -> Tuple[Dict[str, str], float]:
    df_columns = [str(col).lower().strip() for col in df.columns]
    mapping = {}
    confidence_scores = []

    for target_col, aliases in ALIAS_DICT.items():
        best_match, best_score = process.extractOne(aliases[0], df_columns)
        for alias in aliases[1:]:
            match, score = process.extractOne(alias, df_columns)
            if score > best_score:
                best_score, best_match = score, match
        
        if best_score >= 70:
            original_col = [col for col in df.columns if str(col).lower().strip() == best_match][0]
            mapping[target_col] = original_col
            confidence_scores.append(best_score)
        else:
            mapping[target_col] = None

    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
    return mapping, avg_confidence