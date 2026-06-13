import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any


def create_revenue_trend_chart(kpis: Dict[str, Any]) -> go.Figure:
    if 'Monthly_Revenue' not in kpis:
        fig = go.Figure()
        fig.update_layout(
            title="Monthly Revenue Trend (Data Not Available)",
            template="plotly_white"
        )
        return fig

    df = kpis['Monthly_Revenue'].copy()

    if len(df) == 0:
        fig = go.Figure()
        fig.update_layout(
            title="Monthly Revenue Trend (No Data)",
            template="plotly_white"
        )
        return fig

    df['Month'] = df['Month'].astype(str)

    fig = px.line(
        df,
        x='Month',
        y='Revenue',
        markers=True,
        color_discrete_sequence=['#10B981']
    )

    fig.update_layout(
        title="Monthly Revenue Trend",
        xaxis_title="Month",
        yaxis_title="Revenue",
        template="plotly_white"
    )

    return fig


def create_regional_chart(kpis: Dict[str, Any]) -> go.Figure:
    if 'Top_Regions' not in kpis or kpis['Top_Regions'].empty:
        fig = go.Figure()
        fig.update_layout(
            title="Regional Analysis Not Available",
            template="plotly_white"
        )
        return fig

    fig = px.bar(
        kpis['Top_Regions'],
        x='Region',
        y='Revenue',
        text_auto='.2s',
        color_discrete_sequence=['#0F172A']
    )

    fig.update_layout(
        title="Revenue by Top Regions",
        template="plotly_white"
    )

    return fig


def create_product_chart(kpis: Dict[str, Any]) -> go.Figure:
    if 'Top_Products' not in kpis or kpis['Top_Products'].empty:
        fig = go.Figure()
        fig.update_layout(
            title="Product Analysis Not Available",
            template="plotly_white"
        )
        return fig

    fig = px.pie(
        kpis['Top_Products'],
        values='Revenue',
        names='Product',
        color_discrete_sequence=px.colors.sequential.Teal
    )

    fig.update_layout(
        title="Revenue Share by Top Products",
        template="plotly_white"
    )

    return fig


def create_forecast_chart(forecast_data: pd.DataFrame) -> go.Figure:
    if forecast_data is None or len(forecast_data) == 0:
        fig = go.Figure()
        fig.update_layout(
            title="Forecast Not Available",
            template="plotly_white"
        )
        return fig

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=forecast_data['Date'],
            y=forecast_data['Forecast'],
            mode='lines+markers',
            name='Forecast'
        )
    )

    if 'Upper_Bound' in forecast_data.columns:
        fig.add_trace(
            go.Scatter(
                x=forecast_data['Date'],
                y=forecast_data['Upper_Bound'],
                mode='lines',
                showlegend=False
            )
        )

    if 'Lower_Bound' in forecast_data.columns:
        fig.add_trace(
            go.Scatter(
                x=forecast_data['Date'],
                y=forecast_data['Lower_Bound'],
                mode='lines',
                fill='tonexty'
            )
        )

    fig.update_layout(
        title="3-Month Revenue Forecast",
        template="plotly_white"
    )

    return fig


def create_customer_chart(kpis: Dict[str, Any]) -> go.Figure:
    fig = px.pie(
        names=['New Customers', 'Repeat Customers'],
        values=[
            kpis.get('New_Customers', 0),
            kpis.get('Repeat_Customers', 0)
        ],
        color_discrete_sequence=['#334155', '#10B981']
    )

    fig.update_layout(
        title="Customer Distribution",
        template="plotly_white"
    )

    return fig