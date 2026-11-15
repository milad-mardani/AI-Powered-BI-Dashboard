
import pandas as pd
from pathlib import Path


# ==================================================
# 1. PATHS AND DATA LOADING
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR.parent / "data" / "sales_data_clean.csv"

sales_data = pd.read_csv(DATA_FILE)

required_columns = [
    "OrderID",
    "Status",
    "Revenue",
    "Product",
    "Region",
    "OrderDate"
]

missing_columns = [
    column for column in required_columns
    if column not in sales_data.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

sales_data["Status"] = (
    sales_data["Status"].astype(str).str.strip()
)

sales_data["OrderDate"] = pd.to_datetime(
    sales_data["OrderDate"],
    errors="coerce"
)

# Only Completed orders contribute to Revenue and AOV.
completed_df = sales_data[
    sales_data["Status"] == "Completed"
].copy()


# ==================================================
# 2. HELPER FUNCTIONS
# ==================================================

def get_revenue_data():
    return completed_df[
        completed_df["Revenue"].notna()
    ].copy()


def get_total_orders():
    return int(len(sales_data))


def get_total_revenue():
    revenue = get_revenue_data()["Revenue"].sum()
    return round(float(revenue), 2)


def get_completed_orders():
    return int(len(completed_df))


def get_average_order_value():
    revenue_data = get_revenue_data()

    if revenue_data.empty:
        return 0.0

    return round(
        float(revenue_data["Revenue"].mean()),
        2
    )


# ==================================================
# 3. ORDER STATUS ANALYSIS
# ==================================================

def get_order_status_counts():

    statuses = [
        "Completed",
        "Pending",
        "Cancelled"
    ]

    counts = sales_data["Status"].value_counts()

    return {
        status: int(counts.get(status, 0))
        for status in statuses
    }


def get_order_status_percentage():

    total_orders = get_total_orders()

    if total_orders == 0:
        return {
            "Completed": 0.0,
            "Pending": 0.0,
            "Cancelled": 0.0
        }

    counts = get_order_status_counts()

    return {
        status: round(
            (count / total_orders) * 100,
            2
        )
        for status, count in counts.items()
    }


def get_order_status_summary():

    counts = get_order_status_counts()
    percentages = get_order_status_percentage()

    return {
        "total_orders": get_total_orders(),
        "status_breakdown": {
            status: {
                "count": counts[status],
                "percentage": percentages[status]
            }
            for status in counts
        }
    }


def get_pending_orders():
    return get_order_status_counts()["Pending"]


def get_cancelled_orders():
    return get_order_status_counts()["Cancelled"]


# ==================================================
# 4. ORDER PERFORMANCE RATES
# ==================================================

def get_completion_rate():

    total = get_total_orders()

    if total == 0:
        return 0.0

    return round(
        (get_completed_orders() / total) * 100,
        2
    )


def get_pending_rate():

    total = get_total_orders()

    if total == 0:
        return 0.0

    return round(
        (get_pending_orders() / total) * 100,
        2
    )


def get_cancellation_rate():

    total = get_total_orders()

    if total == 0:
        return 0.0

    return round(
        (get_cancelled_orders() / total) * 100,
        2
    )


# ==================================================
# 5. PRODUCT ANALYSIS
# ==================================================

def get_revenue_by_product():

    revenue_data = get_revenue_data()

    result = (
        revenue_data.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    return [
        {
            "product": str(product),
            "revenue": round(float(revenue), 2)
        }
        for product, revenue in result.items()
    ]


def get_best_product():

    products = get_revenue_by_product()

    if not products:
        return None

    return products[0]


def get_lowest_product():

    products = get_revenue_by_product()

    if not products:
        return None

    return products[-1]


def get_top_5_products():
    return get_revenue_by_product()[:5]


def get_product_share(product_name):

    revenue_data = get_revenue_data()
    total_revenue = get_total_revenue()

    if total_revenue == 0:
        return 0.0

    product_revenue = revenue_data.loc[
        revenue_data["Product"].astype(str).str.lower()
        == product_name.lower(),
        "Revenue"
    ].sum()

    return round(
        (float(product_revenue) / total_revenue) * 100,
        2
    )


# ==================================================
# 6. REGIONAL ANALYSIS
# ==================================================

def get_revenue_by_region():

    revenue_data = get_revenue_data()

    result = (
        revenue_data.groupby("Region")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    return [
        {
            "region": str(region),
            "revenue": round(float(revenue), 2)
        }
        for region, revenue in result.items()
    ]


def get_best_region():

    regions = get_revenue_by_region()

    if not regions:
        return None

    return regions[0]


# ==================================================
# 7. MONTHLY REVENUE ANALYSIS
# ==================================================

def get_monthly_revenue_trend():

    revenue_data = get_revenue_data().copy()

    revenue_data = revenue_data.dropna(
        subset=["OrderDate"]
    )

    if revenue_data.empty:
        return []

    revenue_data["Month"] = (
        revenue_data["OrderDate"]
        .dt.to_period("M")
        .astype(str)
    )

    result = (
        revenue_data.groupby("Month")["Revenue"]
        .sum()
        .sort_index()
    )

    return [
        {
            "month": str(month),
            "revenue": round(float(revenue), 2)
        }
        for month, revenue in result.items()
    ]


def get_best_month():

    monthly_data = get_monthly_revenue_trend()

    if not monthly_data:
        return None

    return max(
        monthly_data,
        key=lambda item: item["revenue"]
    )


# ==================================================
# 8. BUSINESS SUMMARY
# ==================================================

def get_business_summary():

    return {
        "total_orders": get_total_orders(),
        "completed_orders": get_completed_orders(),
        "pending_orders": get_pending_orders(),
        "cancelled_orders": get_cancelled_orders(),
        "total_revenue": get_total_revenue(),
        "average_order_value": get_average_order_value(),
        "completion_rate": get_completion_rate(),
        "pending_rate": get_pending_rate(),
        "cancellation_rate": get_cancellation_rate(),
        "best_product": get_best_product(),
        "best_region": get_best_region(),
        "best_month": get_best_month()
    }


# ==================================================
# 9. QUESTION ROUTER
# ==================================================

def route_question(question):

    question = str(question).lower().strip()
    question = " ".join(question.split())

    # ----------------------------------------------
    # Business Summary
    # ----------------------------------------------

    if any(phrase in question for phrase in [
        "business summary",
        "business overview",
        "overall performance",
        "summarize the business",
        "summarize business",
        "give me a summary"
    ]):

        return {
            "metric": "Business Summary",
            "result": get_business_summary()
        }

    # ----------------------------------------------
    # Monthly Revenue Trend
    # ----------------------------------------------

    if any(phrase in question for phrase in [
        "monthly revenue trend",
        "revenue trend",
        "revenue over time",
        "monthly sales trend"
    ]):

        return {
            "metric": "Monthly Revenue Trend",
            "result": get_monthly_revenue_trend()
        }

    # ----------------------------------------------
    # Revenue by Product
    # ----------------------------------------------

    if any(phrase in question for phrase in [
        "revenue by product",
        "product revenue breakdown",
        "sales by product"
    ]):

        return {
            "metric": "Revenue by Product",
            "result": get_revenue_by_product()
        }

    # ----------------------------------------------
    # Revenue by Region
    # ----------------------------------------------

    if any(phrase in question for phrase in [
        "revenue by region",
        "regional revenue",
        "sales by region",
        "compare revenue across all regions",
        "compare regions"
    ]):

        return {
            "metric": "Revenue by Region",
            "result": get_revenue_by_region()
        }

    # ----------------------------------------------
    # Order Status Analysis
    # ----------------------------------------------

    if any(phrase in question for phrase in [
        "order status",
        "order statuses",
        "status distribution",
        "distribution of orders",
        "order breakdown"
    ]):

        return {
            "metric": "Order Status Analysis",
            "result": get_order_status_summary()
        }

    # ----------------------------------------------
    # Status Percentages
    # ----------------------------------------------

    percentage_words = [
        "percentage",
        "percent",
        "rate",
        "proportion"
    ]

    if any(word in question for word in percentage_words):

        percentages = get_order_status_percentage()

        percentage_metrics = {
            "completed": (
                "Completion Rate",
                "Completed"
            ),
            "completion": (
                "Completion Rate",
                "Completed"
            ),
            "pending": (
                "Pending Rate",
                "Pending"
            ),
            "cancelled": (
                "Cancellation Rate",
                "Cancelled"
            ),
            "canceled": (
                "Cancellation Rate",
                "Cancelled"
            ),
            "cancellation": (
                "Cancellation Rate",
                "Cancelled"
            )
        }

        for keyword, (metric_name, status_name) in percentage_metrics.items():

            if keyword in question:

                return {
                    "metric": metric_name,
                    "result": percentages[status_name]
                }

    # ----------------------------------------------
    # Status Counts
    # ----------------------------------------------

    count_words = [
        "how many",
        "number of",
        "count of",
        "count",
        "total number"
    ]

    if any(word in question for word in count_words):

        counts = get_order_status_counts()

        status_aliases = {
            "Completed": ["completed"],
            "Pending": ["pending"],
            "Cancelled": ["cancelled", "canceled"]
        }

        for status, aliases in status_aliases.items():

            if any(alias in question for alias in aliases):

                return {
                    "metric": f"{status} Orders",
                    "result": counts[status]
                }

    # ----------------------------------------------
    # Completion Rate
    # ----------------------------------------------

    if "completion rate" in question:

        return {
            "metric": "Completion Rate",
            "result": get_completion_rate()
        }

    # ----------------------------------------------
    # Cancellation Rate
    # ----------------------------------------------

    if (
        "cancellation rate" in question
        or "cancel rate" in question
    ):

        return {
            "metric": "Cancellation Rate",
            "result": get_cancellation_rate()
        }

    # ----------------------------------------------
    # Pending Rate
    # ----------------------------------------------

    if "pending rate" in question:

        return {
            "metric": "Pending Rate",
            "result": get_pending_rate()
        }

    # ----------------------------------------------
    # Average Order Value
    # ----------------------------------------------

    if any(phrase in question for phrase in [
        "average order value",
        "average value of orders",
        "average order",
        "aov",
        "average basket value"
    ]):

        return {
            "metric": "Average Order Value",
            "result": get_average_order_value()
        }

    # ----------------------------------------------
    # Total Orders
    # ----------------------------------------------

    if any(phrase in question for phrase in [
        "total orders",
        "how many orders",
        "number of orders",
        "order count"
    ]):

        return {
            "metric": "Total Orders",
            "result": get_total_orders()
        }

    # ----------------------------------------------
    # Total Revenue
    # ----------------------------------------------

    if any(phrase in question for phrase in [
        "total revenue",
        "overall revenue",
        "total sales",
        "how much revenue"
    ]):

        return {
            "metric": "Total Revenue",
            "result": get_total_revenue()
        }

    # ----------------------------------------------
    # Best Month
    # ----------------------------------------------

    if any(phrase in question for phrase in [
        "best month",
        "highest revenue month",
        "top month",
        "which month",
        "month with the highest revenue",
        "month generated the highest revenue"
    ]):

        return {
            "metric": "Best Month",
            "result": get_best_month()
        }

    # ----------------------------------------------
    # Best Region
    # ----------------------------------------------

    if any(phrase in question for phrase in [
        "best region",
        "highest revenue region",
        "top region",
        "which region",
        "region with the highest revenue",
        "region generated the highest revenue"
    ]):

        return {
            "metric": "Best Region",
            "result": get_best_region()
        }

    # ----------------------------------------------
    # Best Product
    # ----------------------------------------------

    best_product_phrases = [
        "best product",
        "highest revenue product",
        "top product",
        "which product generated",
        "highest selling product",
        "product with the highest revenue",
        "product has the highest revenue",
        "product that has the highest revenue",
        "product generates the highest revenue",
        "product generated the highest revenue",
        "which product has the highest sales",
        "best performing product",
        "top performing product",
        "best-selling product",
        "best selling product"
    ]

    if any(phrase in question for phrase in best_product_phrases):

        return {
            "metric": "Best Product",
            "result": get_best_product()
        }

    # ----------------------------------------------
    # Lowest Product
    # ----------------------------------------------

    lowest_product_phrases = [
        "lowest product",
        "worst product",
        "lowest revenue product",
        "product with the lowest revenue",
        "product has the lowest revenue",
        "product with the least revenue",
        "lowest performing product",
        "worst performing product"
    ]

    if any(phrase in question for phrase in lowest_product_phrases):

        return {
            "metric": "Lowest Product",
            "result": get_lowest_product()
        }

    # ----------------------------------------------
    # Product Revenue Share
    # ----------------------------------------------

    if (
        "share" in question
        or "percentage of revenue" in question
    ):

        for product in sales_data["Product"].dropna().unique():

            if str(product).lower() in question:

                return {
                    "metric": f"{product} Revenue Share",
                    "result": get_product_share(str(product))
                }

    # ----------------------------------------------
    # Top 5 Products
    # ----------------------------------------------

    if any(phrase in question for phrase in [
        "top 5 products",
        "top five products",
        "five best products",
        "top products"
    ]):

        return {
            "metric": "Top 5 Products",
            "result": get_top_5_products()
        }

    return None


# ==================================================
# 10. TESTING
# ==================================================

if __name__ == "__main__":

    print("\n===== PYTHON ANALYTICAL ENGINE =====")

    print("Total Orders:", get_total_orders())
    print("Total Revenue:", get_total_revenue())
    print("Completed Orders:", get_completed_orders())
    print("Pending Orders:", get_pending_orders())
    print("Cancelled Orders:", get_cancelled_orders())

    print("Average Order Value:", get_average_order_value())

    print("Completion Rate:", get_completion_rate())
    print("Pending Rate:", get_pending_rate())
    print("Cancellation Rate:", get_cancellation_rate())

    print("Order Status:", get_order_status_summary())

    print("Best Product:", get_best_product())
    print("Lowest Product:", get_lowest_product())
    print("Top 5 Products:", get_top_5_products())
    print("Revenue by Product:", get_revenue_by_product())

    print("Best Region:", get_best_region())
    print("Revenue by Region:", get_revenue_by_region())

    print("Best Month:", get_best_month())
    print("Monthly Revenue Trend:", get_monthly_revenue_trend())

    print("\n===== QUESTION ROUTER TEST =====")

    test_questions = [
        "What is total revenue?",
        "How many orders are there?",
        "What is the average order value?",
        "How many completed orders are there?",
        "How many pending orders are there?",
        "How many cancelled orders are there?",
        "What is the order status distribution?",
        "What is the completion rate?",
        "What is the cancellation rate?",
        "What is the pending rate?",
        "Which product generated the highest revenue?",
        "Which product has the highest revenue?",
        "What is the product with the highest revenue?",
        "What is the best-selling product?",
        "Which product has the lowest revenue?",
        "Show revenue by product",
        "Show me the top 5 products",
        "Which region generated the highest revenue?",
        "Show revenue by region",
        "Compare revenue across all regions",
        "Which month had the highest revenue?",
        "Show the monthly revenue trend",
        "Give me a business summary"
    ]

    for question in test_questions:

        result = route_question(question)

        print(f"\n{question}")
        print(result)
