# WMS Dashboard Design

## 1. Overview

This document outlines the design for the Warehouse Management System (WMS) dashboard to be built using Teable.io. The purpose of this dashboard is to provide a clear, at-a-glance overview of key sales and inventory metrics, enabling non-technical users to make data-driven decisions.

The dashboard will be built using the data from the `SalesData`, `SKUs`, and `Products` tables in our Teable base.

## 2. Key Metrics & Visualizations

The dashboard will be composed of several widgets, each visualizing a key performance indicator (KPI).

### Metric 1: Total Sales Revenue
- **Widget Type:** Statistic / Big Number
- **Description:** A single, prominent number showing the total revenue from all sales in a given period.
- **Data Source:** A "sum" aggregation on the `price` column of the `SalesData` table.

### Metric 2: Total Units Sold
- **Widget Type:** Statistic / Big Number
- **Description:** A single number showing the total quantity of all items sold.
- **Data Source:** A "sum" aggregation on the `quantity` column of the `SalesData` table.

### Metric 3: Sales Trend Over Time
- **Widget Type:** Line Chart
- **Description:** A line chart showing the total sales revenue per day or week. This helps to identify trends, seasonality, and the impact of marketing campaigns.
- **Data Source:**
  - **X-Axis:** The `order_date` field from `SalesData`, grouped by day or week.
  - **Y-Axis:** A "sum" aggregation of the `price` column.

### Metric 4: Sales by Product (MSKU)
- **Widget Type:** Bar Chart (or Pie Chart)
- **Description:** A bar chart displaying the top-selling products based on revenue. This is crucial for identifying the most profitable items.
- **Data Source:**
  - **X-Axis:** The `product_link` (showing the MSKU) from the `SalesData` table.
  - **Y-Axis:** A "sum" aggregation of the `price` column.
  - **Sorting:** Sorted in descending order.

### Metric 5: Sales by Marketplace
- **Widget Type:** Pie Chart
- **Description:** A pie chart showing the percentage of total sales revenue coming from each marketplace (e.g., Amazon, Flipkart, Meesho).
- **Data Source:** This requires adding a `source_marketplace` column to the `SalesData` table during processing.
  - **Segments:** The `source_marketplace` column.
  - **Value:** A "sum" aggregation of the `price` column.

### Metric 6: Detailed Sales Records
- **Widget Type:** Table
- **Description:** A searchable and filterable table view of the most recent sales records. This allows users to drill down into specific orders.
- **Data Source:** A direct view of the `SalesData` table, showing columns like `order_date`, `sku_link`, `quantity`, and `price`.

## 3. Dashboard Layout Sketch

The dashboard will be organized in a 2x3 grid layout for clarity.

|                                         |                                            |
| --------------------------------------- | ------------------------------------------ |
| **Total Sales Revenue** (Statistic)     | **Total Units Sold** (Statistic)           |
| **Sales Trend Over Time** (Line Chart)  | **Sales by Product (MSKU)** (Bar Chart)    |
| **Sales by Marketplace** (Pie Chart)    | **Detailed Sales Records** (Table)         |

This layout places the most important, high-level numbers at the top, followed by trend and breakdown charts, with the detailed data table at the bottom for drill-down analysis.
