from typing import Dict, Any, List

def generate_insights(kpis: Dict[str, Any], df: pd.DataFrame) -> List[str]:
    insights = []
    mom = kpis.get('MoM_Growth', 0)
    
    if mom > 5:
        insights.append(f"Revenue showed strong momentum, increasing by {mom:.1f}% compared to the previous month.")
    elif mom < -5:
        insights.append(f"Revenue experienced a contraction of {abs(mom):.1f}% month-over-month, warranting immediate investigation.")
    else:
        insights.append(f"Revenue remained relatively stable with a {mom:.1f}% month-over-month change.")

    if 'Top_Products' in kpis and not kpis['Top_Products'].empty:
        top = kpis['Top_Products'].iloc[0]
        pct = (top['Revenue'] / kpis['Total_Revenue']) * 100
        insights.append(f"'{top['Product']}' is the primary revenue driver, contributing {pct:.1f}% of total sales.")
        if pct > 40:
            insights.append("WARNING: High revenue concentration risk exists on a single product.")

    if kpis.get('Repeat_Customers', 0) > kpis.get('New_Customers', 0):
        insights.append("Customer retention is strong, with repeat customers outnumbering new acquisitions.")
    else:
        insights.append("Customer acquisition is outpacing retention, indicating growth but potential churn risks.")
        
    return insights