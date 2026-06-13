import pandas as pd
from typing import Dict, Any


def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    kpis = {}

    # --------------------------------
    # Capability Detection
    # --------------------------------
    capabilities = {
        "date": "Date" in df.columns,
        "revenue": "Revenue" in df.columns,
        "customer": "Customer" in df.columns,
        "product": "Product" in df.columns,
        "region": "Region" in df.columns,
        "salesperson": "Salesperson" in df.columns,
        "orders": "Order_ID" in df.columns,
    }

    kpis["Capabilities"] = capabilities

    # --------------------------------
    # Revenue KPIs
    # --------------------------------
    if capabilities["revenue"]:
        kpis["Total_Revenue"] = float(df["Revenue"].sum())
    else:
        kpis["Total_Revenue"] = 0.0

    # --------------------------------
    # Date-Based KPIs
    # --------------------------------
    if capabilities["date"]:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        df = df.dropna(subset=["Date"])

        if len(df) > 0:
            df["Month"] = df["Date"].dt.to_period("M")
            df["Quarter"] = df["Date"].dt.to_period("Q")

            if capabilities["revenue"]:
                monthly_revenue = (
                    df.groupby("Month")["Revenue"]
                    .sum()
                    .reset_index()
                )

                kpis["Monthly_Revenue"] = monthly_revenue

                if len(monthly_revenue) > 1:
                    monthly_revenue = monthly_revenue.sort_values("Month")

                    monthly_revenue["Prev_Revenue"] = (
                        monthly_revenue["Revenue"].shift(1)
                    )

                    monthly_revenue["MoM_Growth"] = (
                        (
                            monthly_revenue["Revenue"]
                            - monthly_revenue["Prev_Revenue"]
                        )
                        / monthly_revenue["Prev_Revenue"]
                    ) * 100

                    latest_growth = monthly_revenue[
                        "MoM_Growth"
                    ].dropna()

                    kpis["MoM_Growth"] = (
                        float(latest_growth.iloc[-1])
                        if len(latest_growth) > 0
                        else 0.0
                    )
                else:
                    kpis["MoM_Growth"] = 0.0

    else:
        kpis["MoM_Growth"] = 0.0

    # --------------------------------
    # Customer KPIs
    # --------------------------------
    if capabilities["customer"]:
        kpis["Total_Customers"] = int(
            df["Customer"].nunique()
        )
    else:
        kpis["Total_Customers"] = 0

    if capabilities["customer"] and capabilities["orders"]:
        customer_orders = (
            df.groupby("Customer")["Order_ID"]
            .nunique()
        )

        kpis["New_Customers"] = int(
            (customer_orders == 1).sum()
        )

        kpis["Repeat_Customers"] = int(
            (customer_orders > 1).sum()
        )

    else:
        kpis["New_Customers"] = 0
        kpis["Repeat_Customers"] = 0

    # --------------------------------
    # Order KPIs
    # --------------------------------
    if capabilities["orders"]:
        kpis["Total_Orders"] = int(
            df["Order_ID"].nunique()
        )
    else:
        kpis["Total_Orders"] = len(df)

    if kpis["Total_Orders"] > 0:
        kpis["AOV"] = (
            kpis["Total_Revenue"]
            / kpis["Total_Orders"]
        )
    else:
        kpis["AOV"] = 0.0

    # --------------------------------
    # Product Analysis
    # --------------------------------
    if capabilities["product"] and capabilities["revenue"]:
        kpis["Top_Products"] = (
            df.groupby("Product")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

    # --------------------------------
    # Region Analysis
    # --------------------------------
    if capabilities["region"] and capabilities["revenue"]:
        kpis["Top_Regions"] = (
            df.groupby("Region")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

    # --------------------------------
    # Salesperson Analysis
    # --------------------------------
    if capabilities["salesperson"] and capabilities["revenue"]:
        kpis["Top_Salespersons"] = (
            df.groupby("Salesperson")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

    # --------------------------------
    # Available Analysis Summary
    # --------------------------------
    available_analysis = []

    if capabilities["revenue"]:
        available_analysis.append(
            "Revenue Analysis"
        )

    if capabilities["date"]:
        available_analysis.append(
            "Trend Analysis"
        )

    if capabilities["customer"]:
        available_analysis.append(
            "Customer Analysis"
        )

    if capabilities["product"]:
        available_analysis.append(
            "Product Analysis"
        )

    if capabilities["region"]:
        available_analysis.append(
            "Regional Analysis"
        )

    if capabilities["salesperson"]:
        available_analysis.append(
            "Salesperson Analysis"
        )

    kpis["Available_Analysis"] = available_analysis

    return kpis