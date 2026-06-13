# Architecture Documentation

## Overview
The Sales KPI Intelligence Dashboard is a modular, local-first Streamlit application designed to transform raw tabular data into executive-ready insights without cloud dependencies.

## Module Responsibilities
- **`data_loader.py`**: Handles secure, local parsing of CSV and Excel files.
- **`column_mapper.py`**: Uses fuzzy string matching (`fuzzywuzzy`) against a predefined alias dictionary to auto-map user columns to system standards.
- **`data_cleaner.py`**: Executes a pipeline of deduplication, type coercion, missing value imputation, and generates a quantifiable Data Quality Score (0-100).
- **`kpi_engine.py`**: Computes hierarchical metrics (Revenue, Customer, Sales, Growth) using vectorized Pandas operations.
- **`forecasting.py`**: Implements a Weighted Moving Average (WMA) with trend adjustment for robust, dependency-free short-term forecasting.
- **`insights_engine.py` & `recommendation_engine.py`**: Rule-based natural language generation (NLG) that translates statistical deltas into management-consulting-style commentary.
- **`report_generator.py`**: Uses `reportlab` to compile all dashboard state into a branded, downloadable PDF.

## Data Flow
1. Upload → 2. Fuzzy Mapping → 3. Validation/Cleaning → 4. KPI Calculation → 5. Insight Generation → 6. Visualization & PDF Export.