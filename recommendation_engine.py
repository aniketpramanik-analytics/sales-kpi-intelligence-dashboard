from typing import Dict, Any, List

def generate_recommendations(kpis: Dict[str, Any], insights: List[str]) -> List[Dict[str, str]]:
    recs = []
    mom = kpis.get('MoM_Growth', 0)
    
    if mom < 0:
        recs.append({'category': 'Revenue', 'action': 'Launch targeted promotional campaigns or bundle offerings to stimulate immediate demand.'})
    else:
        recs.append({'category': 'Revenue', 'action': 'Capitalize on current momentum by scaling successful marketing channels.'})

    if 'Top_Products' in kpis and not kpis['Top_Products'].empty:
        top = kpis['Top_Products'].iloc[0]
        if (top['Revenue'] / kpis['Total_Revenue']) > 0.35:
            recs.append({'category': 'Risk Management', 'action': f"Diversify the product portfolio. Over-reliance on '{top['Product']}' poses a significant business risk."})

    if kpis.get('New_Customers', 0) > kpis.get('Repeat_Customers', 0):
        recs.append({'category': 'Customer', 'action': 'Implement or enhance customer loyalty programs to improve retention rates.'})
    else:
        recs.append({'category': 'Customer', 'action': 'Leverage the strong repeat customer base for referral programs and upselling initiatives.'})

    if 'Top_Regions' in kpis and len(kpis['Top_Regions']) > 1:
        bottom = kpis['Top_Regions'].iloc[-1]
        recs.append({'category': 'Regional', 'action': f"Conduct a root-cause analysis in the '{bottom['Region']}' region to identify operational headwinds."})

    return recs