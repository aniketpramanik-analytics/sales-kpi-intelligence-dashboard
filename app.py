import streamlit as st
import pandas as pd
import sys, os

sys.path.append(os.path.abspath("modules"))
from data_loader import load_data
from column_mapper import map_columns, REQUIRED_COLUMNS
from data_cleaner import clean_data
from kpi_engine import calculate_kpis
from forecasting import forecast_sales
from insights_engine import generate_insights
from recommendation_engine import generate_recommendations
from analyst_notes import generate_analyst_notes
from charts import create_revenue_trend_chart, create_regional_chart, create_product_chart, create_forecast_chart, create_customer_chart
from report_generator import generate_pdf_report
from utils import format_currency, format_percentage, format_number

st.set_page_config(page_title="Sales KPI Intelligence Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.title("📊 Sales KPI Intelligence Dashboard")
    st.markdown("Transform raw sales data into executive-level business insights, forecasting, and management reports.")

    st.sidebar.header("Data Source")
    uploaded_file = st.sidebar.file_uploader("Upload Sales Data", type=['csv', 'xlsx', 'xls'])

    if uploaded_file is not None:
        if 'df_raw' not in st.session_state:
            st.session_state.df_raw = load_data(uploaded_file)
        
        if st.session_state.df_raw is not None:
            st.sidebar.success("File uploaded successfully!")
            
            if 'mapping' not in st.session_state:
                mapping, confidence = map_columns(st.session_state.df_raw)
                st.session_state.mapping = mapping

            st.sidebar.markdown("---")
            st.sidebar.subheader("Smart Column Mapping")
            
            new_mapping = {}
            all_good = True
            for target in REQUIRED_COLUMNS + ['Quantity', 'Product', 'Category', 'Customer', 'Region', 'Salesperson', 'Order_ID']:
                current_val = st.session_state.mapping.get(target, None)
                options = ["None"] + list(st.session_state.df_raw.columns)
                idx = options.index(str(current_val)) if str(current_val) in options else 0
                
                selected = st.sidebar.selectbox(f"Map to **{target}**", options=options, index=idx, key=f"map_{target}")
                if selected != "None":
                    new_mapping[target] = selected
                elif target in REQUIRED_COLUMNS:
                    all_good = False
                    st.sidebar.error(f"⚠️ **{target}** is required!")
            
            st.session_state.mapping = new_mapping

            if st.sidebar.button("Process & Clean Data"):
                if all_good:
                    with st.spinner("Cleaning and validating data..."):
                        df_clean, quality_report = clean_data(st.session_state.df_raw, st.session_state.mapping)
                        st.session_state.df_clean = df_clean
                        st.session_state.quality_report = quality_report
                        st.session_state.kpis = calculate_kpis(df_clean)
                        st.session_state.forecast = forecast_sales(df_clean)
                        st.session_state.insights = generate_insights(st.session_state.kpis, df_clean)
                        st.session_state.recommendations = generate_recommendations(st.session_state.kpis, st.session_state.insights)
                        st.session_state.notes = generate_analyst_notes(st.session_state.kpis, st.session_state.insights, st.session_state.recommendations)
                        st.sidebar.success("Data processed successfully!")
                        st.rerun()
                else:
                    st.sidebar.error("Please map all required columns before processing.")

            if 'df_clean' in st.session_state:
                df = st.session_state.df_clean
                kpis = st.session_state.kpis
                quality_report = st.session_state.quality_report
                
                st.sidebar.markdown("---")
                st.sidebar.subheader("Global Filters")
                date_range = st.sidebar.date_input("Date Range", value=(df['Date'].min().date(), df['Date'].max().date()), min_value=df['Date'].min().date(), max_value=df['Date'].max().date())
                region_filter = st.sidebar.multiselect("Region", options=df['Region'].unique().tolist() if 'Region' in df.columns else [], default=df['Region'].unique().tolist() if 'Region' in df.columns else [])
                
                mask = (df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])
                if 'Region' in df.columns and region_filter:
                    mask &= df['Region'].isin(region_filter)
                df_filtered = df[mask].copy()
                kpis_filtered = calculate_kpis(df_filtered)

                # Section 1: Executive Summary
                st.markdown("### 📈 Executive Summary")
                col1, col2, col3, col4 = st.columns(4)
                with col1: st.metric("Total Revenue", format_currency(kpis_filtered['Total_Revenue']), delta=format_percentage(kpis_filtered.get('MoM_Growth', 0)))
                with col2: st.metric("Total Orders", format_number(kpis_filtered['Total_Orders']))
                with col3: st.metric("Total Customers", format_number(kpis_filtered['Total_Customers']))
                with col4: st.metric("Avg Order Value", format_currency(kpis_filtered['AOV']))

                score = quality_report['quality_score']
                color_class = "quality-score-excellent" if score >= 90 else "quality-score-good" if score >= 75 else "quality-score-moderate" if score >= 50 else "quality-score-poor"
                st.markdown(f"""
                <div class="executive-card {color_class}">
                    <h4>Data Quality Score: {score}/100 ({quality_report['rating']})</h4>
                    <p>{quality_report['commentary'][0]}</p>
                    <small>Rows processed: {quality_report['initial_rows']} | Duplicates removed: {quality_report['duplicates_removed']} | Invalid dates handled: {quality_report['invalid_dates']}</small>
                </div>
                """, unsafe_allow_html=True)

                # Section 2: Revenue Analysis
                st.markdown("### 💰 Revenue Analysis")
                col1, col2 = st.columns(2)
                with col1: st.plotly_chart(create_revenue_trend_chart(kpis_filtered), use_container_width=True)
                with col2: st.plotly_chart(create_regional_chart(kpis_filtered), use_container_width=True)

                # Section 3: Sales Performance
                st.markdown("### 🏆 Sales Performance")
                col1, col2 = st.columns(2)
                with col1: st.plotly_chart(create_product_chart(kpis_filtered), use_container_width=True)
                with col2:
                    if 'Top_Salespersons' in kpis_filtered and not kpis_filtered['Top_Salespersons'].empty:
                        import plotly.express as px
                        fig = px.bar(kpis_filtered['Top_Salespersons'], x='Salesperson', y='Revenue', text_auto='.2s', color_discrete_sequence=['#334155'])
                        fig.update_layout(title="Top Salespersons", template="plotly_white")
                        st.plotly_chart(fig, use_container_width=True)

                # Section 4: Customer Analysis
                st.markdown("### 👥 Customer Analysis")
                col1, col2 = st.columns(2)
                with col1: st.plotly_chart(create_customer_chart(kpis_filtered), use_container_width=True)
                with col2:
                    st.markdown("#### KPI Commentary")
                    for insight in st.session_state.insights[:3]:
                        st.markdown(f"• {insight}")

                # Section 5: Forecasting
                st.markdown("### 🔮 3-Month Revenue Forecast")
                st.plotly_chart(create_forecast_chart(st.session_state.forecast['forecast_df']), use_container_width=True)
                st.info(f"Forecast Method: {st.session_state.forecast['method']}")

                # Section 6: Recommendations & Notes
                st.markdown("### 📋 Executive Recommendations & Analyst Notes")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Recommendations")
                    for rec in st.session_state.recommendations:
                        st.markdown(f"**{rec['category']}**: {rec['action']}")
                with col2:
                    st.markdown("#### Analyst Notes")
                    st.markdown(f"**Key Findings:** {st.session_state.notes['key_findings']}")
                    st.markdown(f"**Risks:** {st.session_state.notes['risks']}")
                    st.markdown(f"**Opportunities:** {st.session_state.notes['opportunities']}")

                # Export
                st.markdown("---")
                if st.button("📥 Download Professional PDF Report"):
                    with st.spinner("Generating report..."):
                        pdf_bytes = generate_pdf_report(kpis_filtered, st.session_state.insights, st.session_state.recommendations, st.session_state.notes, quality_report)
                        st.download_button(label="Download Business Report (PDF)", data=pdf_bytes, file_name="Executive_Sales_Report.pdf", mime="application/pdf")
            else:
                st.info("Please map the columns and click 'Process & Clean Data' to generate the dashboard.")
    else:
        st.info("👈 Please upload a CSV or Excel file from the sidebar to begin.")

if __name__ == "__main__":
    main()