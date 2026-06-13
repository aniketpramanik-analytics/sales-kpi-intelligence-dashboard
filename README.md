# Sales KPI Intelligence Dashboard

A professional-grade, local-first analytics application that transforms raw sales data into executive-level business insights, KPI reporting, forecasting, and downloadable management reports.

## 🚀 Features
- **Smart Column Mapping**: Auto-detects columns using fuzzy matching (supports aliases like "Sales", "Revenue", "Amount").
- **Data Quality Engine**: Automatically cleans data, removes duplicates, handles missing values, and generates a 0-100 Quality Score.
- **Automated KPIs**: Calculates Revenue, Customer, Sales, and Growth metrics dynamically.
- **Forecasting**: 3-month weighted moving average forecast with confidence intervals.
- **Executive Insights**: Auto-generated plain-language business commentary, risks, and recommendations.
- **PDF Export**: One-click generation of a branded, management-consulting-style PDF report.

## 🛠️ Installation
1. Ensure you have Python 3.9+ installed.
2. Clone or download this repository.
3. Open your terminal in the `sales_kpi_dashboard` directory.
4. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate