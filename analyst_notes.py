from typing import Dict, Any, List

def generate_analyst_notes(kpis: Dict[str, Any], insights: List[str], recommendations: List[Dict[str, str]]) -> Dict[str, str]:
    findings = [i for i in insights if "strong momentum" in i.lower() or "primary revenue driver" in i.lower()]
    risks = [i for i in insights if "WARNING" in i or "contraction" in i.lower()]
    
    return {
        'key_findings': " • ".join(findings) if findings else "Revenue trends are stable. Top products and regions are performing as expected.",
        'risks': " • ".join(risks) if risks else "No immediate critical risks detected. Continue monitoring market conditions.",
        'opportunities': "Strong customer loyalty presents a prime opportunity for upselling and referral program expansion." if kpis.get('Repeat_Customers', 0) > kpis.get('New_Customers', 0) else "High new customer acquisition indicates market demand; optimize onboarding to convert to repeat buyers.",
        'recommended_actions': " • ".join([r['action'] for r in recommendations[:2]])
    }