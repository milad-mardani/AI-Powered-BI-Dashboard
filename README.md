# AI-Powered BI Dashboard

An AI-powered Business Intelligence solution that combines Python-based data analytics, local Generative AI (Ollama), Streamlit, and Microsoft Power BI to transform sales data into interactive business insights.

## Project Overview

The AI-Powered BI Dashboard enables users to ask business questions in natural language and receive data-driven answers supported by Python analytics and AI-generated explanations.

Instead of manually writing queries or analyzing reports, users can submit business questions through a Streamlit interface.

The Python Analytical Engine calculates accurate business metrics, while a locally running Large Language Model (LLM) generates natural-language explanations based on verified analytical results.

The latest question and its corresponding answer are exported to a CSV file, which is connected to Microsoft Power BI Desktop.

## Key Features

- **Natural Language Question Input:** Submit business questions through a Streamlit web interface.
- **Python-Based Analytics:** Calculate business metrics using Python and Pandas.
- **Local Generative AI:** Generate business explanations using Ollama and Qwen 2.5.
- **Verified Analytical Results:** Python performs calculations; the LLM only explains the calculated results.
- **Power BI Integration:** Export the latest business insight to CSV for Power BI reporting.
- **Latest Result Management:** Each new supported question replaces the previous question and answer in the output CSV.
- **Local Execution:** The application uses a locally running Ollama model instead of a cloud-based LLM API.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Pandas | Data processing and analysis |
| Streamlit | User interface |
| Ollama | Local LLM execution |
| Qwen 2.5:3B | AI-powered explanations |
| Microsoft Power BI Desktop | Business intelligence dashboard |
| CSV | Data exchange between Python and Power BI |

## System Architecture

The application follows a structured workflow:

1. **User Input (Streamlit)**  
   The user enters a business question through the Streamlit interface.

2. **Analytical Engine (Python)**  
   The question is processed by the question router. Python calculates the relevant business metrics using the sales dataset.

3. **AI Explanation (Ollama)**  
   The verified analytical results are converted into a business explanation using the local Qwen 2.5:3B model.

4. **CSV Export**  
   The latest question, analytical metric, explanation, source, and generation timestamp are exported to a CSV file.

5. **Power BI Dashboard**  
   Power BI reads the exported CSV file. After refreshing the dataset, the latest question and AI-generated explanation appear in the dashboard.

### Architecture Flow

```text
User
  |
  v
Streamlit Interface
  |
  v
Python Analytical Engine
  |
  v
Verified Business Results
  |
  v
Ollama (Qwen 2.5:3B)
  |
  v
AI Business Explanation
  |
  v
CSV Export
  |
  v
Microsoft Power BI Desktop
  |
  v
Refresh Dashboard
```

## Supported Business Analytics

The analytical engine currently supports the following business questions and metrics.

### 1. Business Performance

- Business Summary
- Total Revenue
- Total Orders
- Average Order Value (AOV)

### 2. Product Analytics

- Best Product by Revenue
- Lowest Product by Revenue
- Revenue by Product
- Top 5 Products
- Product Revenue Share

### 3. Regional Analytics

- Best Performing Region
- Revenue by Region
- Regional Revenue Comparison

### 4. Monthly Analytics

- Monthly Revenue Trend
- Best Month by Revenue

### 5. Order Analytics

- Total Completed Orders
- Total Pending Orders
- Total Cancelled Orders
- Order Status Distribution
- Completion Rate
- Pending Rate
- Cancellation Rate

## Project Structure

```text
AI-Powered-BI-Dashboard/
│
├── data/
│   ├── sales_data.csv
│   └── sales_data_clean.csv
│
├── notebooks/
│   ├── ai_business_analyst.py
│   ├── analytical_engine.py
│   ├── data_cleaning.py
│   ├── exploratory_data_analysis.py
│   ├── export_powerbi_data.py
│   └── streamlit_app.py
│
├── powerbi_data/
│   ├── ai_business_insights.csv
│   ├── dashboard_summary.csv
│   ├── kpi_summary.csv
│   ├── monthly_revenue.csv
│   ├── order_status.csv
│   ├── product_revenue.csv
│   └── region_revenue.csv
│
├── AI_Powered_BI_Dashboard.pbix
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/milad-mardani/AI-Powered-BI-Dashboard.git
```

```bash
cd AI-Powered-BI-Dashboard
```

### 2. Install Dependencies

Activate your Python environment and install the required packages:

```bash
pip install -r requirements.txt
```

Make sure the following main packages are available:

```bash
pip install pandas ollama streamlit
```

### 3. Install and Run Ollama

Install Ollama from:

https://ollama.com/

Download the required model:

```bash
ollama pull qwen2.5:3b
```

Verify that the model is available:

```bash
ollama list
```

Make sure the Ollama service is running before starting the application.

### 4. Run the Streamlit Application

Open a terminal in the `notebooks` directory and execute:

```bash
python -m streamlit run streamlit_app.py
```

The Streamlit application will open in your browser.

### 5. Ask Business Questions

Enter a supported business question in the Streamlit interface.

Example:

```text
Which product has the highest revenue?
```

The application will:

- Analyze the question using Python.
- Calculate the verified result.
- Generate an AI-powered explanation using Ollama.
- Export the latest question and answer to the Power BI CSV file.

### 6. Refresh Power BI

Open:

```text
AI_Powered_BI_Dashboard.pbix
```

In Power BI Desktop:

1. Navigate to the Home tab.
2. Click Refresh.
3. Review the updated business insight.

The latest supported question and answer will replace the previous result in the connected CSV file.

## Dataset

The project uses a sales dataset containing 1,000 records.

Main dataset columns:

| Column | Description |
|---|---|
| OrderID | Unique order identifier |
| OrderDate | Order date |
| CustomerID | Customer identifier |
| Product | Product name |
| Category | Product category |
| Quantity | Quantity sold |
| UnitPrice | Unit price |
| Revenue | Order revenue |
| Region | Sales region |
| Status | Order status |

### Data Processing Rules

- Revenue is calculated and validated using Quantity × UnitPrice.
- Only Completed orders contribute to Total Revenue and Average Order Value.
- Pending and Cancelled orders are included in order-status analysis.
- Python performs the numerical calculations before the results are passed to the LLM.

## AI Reliability and Data Validation

The project follows a separation-of-responsibilities approach:

**Python is responsible for:**
- Numerical calculations
- Aggregations
- Business metrics
- Analytical results

**The LLM is responsible for:**
- Explaining analytical results
- Generating readable business insights
- Converting verified results into natural language

The AI model is not responsible for calculating business metrics or independently generating numerical business results.

This design helps reduce unsupported numerical claims and keeps analytical calculations separate from AI-generated explanations.

## Current Limitations

- The question router supports a predefined set of business topics and question patterns.
- Questions outside the supported topics are not processed.
- The current implementation exports only the latest supported question and answer rather than maintaining conversation history.
- Power BI Desktop requires a manual Refresh to display the latest exported result.
- The application currently focuses on sales and revenue analytics.
- The LLM explanation depends on the availability of the local Ollama service.

## Future Improvements

Potential future enhancements include:

- Expanding natural-language question understanding.
- Supporting additional business datasets.
- Adding more advanced business KPIs.
- Improving AI-generated business recommendations.
- Automating Power BI data refresh.
- Expanding interactive analytical capabilities.

## Author

**Milad Mardani**

GitHub: https://github.com/milad-mardani

LinkedIn: https://www.linkedin.com/in/miladmardani/

## Project Purpose

This project demonstrates how Python analytics, local Generative AI, and Business Intelligence tools can work together to build an AI-powered business analysis workflow.
