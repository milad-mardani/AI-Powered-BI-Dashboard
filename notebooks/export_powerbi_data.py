
import pandas as pd
from pathlib import Path

# ==================================================
# 1. IMPORT ANALYTICAL ENGINE
# ==================================================

from analytical_engine import (
    get_total_orders,
    get_total_revenue,
    get_completed_orders,
    get_pending_orders,
    get_cancelled_orders,
    get_average_order_value,
    get_completion_rate,
    get_pending_rate,
    get_cancellation_rate,
    get_order_status_summary,
    get_revenue_by_product,
    get_revenue_by_region,
    get_monthly_revenue_trend,
    get_best_product,
    get_best_region,
    get_best_month
)


# ==================================================
# 2. OUTPUT DIRECTORY
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR.parent / "powerbi_data"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==================================================
# 3. KPI SUMMARY EXPORT
# ==================================================

def export_kpi_summary():

    best_product = get_best_product()
    best_region = get_best_region()
    best_month = get_best_month()

    data = {
        "TotalOrders": get_total_orders(),
        "TotalRevenue": get_total_revenue(),
        "CompletedOrders": get_completed_orders(),
        "PendingOrders": get_pending_orders(),
        "CancelledOrders": get_cancelled_orders(),
        "AverageOrderValue": get_average_order_value(),
        "CompletionRate": get_completion_rate(),
        "PendingRate": get_pending_rate(),
        "CancellationRate": get_cancellation_rate(),

        "BestProduct": (
            best_product["product"]
            if best_product else None
        ),

        "BestProductRevenue": (
            best_product["revenue"]
            if best_product else 0
        ),

        "BestRegion": (
            best_region["region"]
            if best_region else None
        ),

        "BestRegionRevenue": (
            best_region["revenue"]
            if best_region else 0
        ),

        "BestMonth": (
            best_month["month"]
            if best_month else None
        ),

        "BestMonthRevenue": (
            best_month["revenue"]
            if best_month else 0
        )
    }

    df = pd.DataFrame([data])

    file_path = OUTPUT_DIR / "kpi_summary.csv"

    df.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig"
    )

    print("Created:", file_path.name)


# ==================================================
# 4. MONTHLY REVENUE EXPORT
# ==================================================

def export_monthly_revenue():

    monthly_data = get_monthly_revenue_trend()

    df = pd.DataFrame(monthly_data)

    if df.empty:
        df = pd.DataFrame(
            columns=["month", "revenue", "month_start"]
        )
    else:
        df["month_start"] = pd.to_datetime(
            df["month"] + "-01"
        )

        df = df.rename(
            columns={
                "month": "Month",
                "revenue": "Revenue"
            }
        )

        df = df[
            ["Month", "month_start", "Revenue"]
        ]

    file_path = OUTPUT_DIR / "monthly_revenue.csv"

    df.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig"
    )

    print("Created:", file_path.name)


# ==================================================
# 5. PRODUCT REVENUE EXPORT
# ==================================================

def export_product_revenue():

    product_data = get_revenue_by_product()

    df = pd.DataFrame(product_data)

    if df.empty:
        df = pd.DataFrame(
            columns=["product", "revenue"]
        )

    df = df.rename(
        columns={
            "product": "Product",
            "revenue": "Revenue"
        }
    )

    file_path = OUTPUT_DIR / "product_revenue.csv"

    df.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig"
    )

    print("Created:", file_path.name)


# ==================================================
# 6. REGIONAL REVENUE EXPORT
# ==================================================

def export_region_revenue():

    region_data = get_revenue_by_region()

    df = pd.DataFrame(region_data)

    if df.empty:
        df = pd.DataFrame(
            columns=["region", "revenue"]
        )

    df = df.rename(
        columns={
            "region": "Region",
            "revenue": "Revenue"
        }
    )

    file_path = OUTPUT_DIR / "region_revenue.csv"

    df.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig"
    )

    print("Created:", file_path.name)


# ==================================================
# 7. ORDER STATUS EXPORT
# ==================================================

def export_order_status():

    status_data = get_order_status_summary()

    rows = []

    for status, values in status_data[
        "status_breakdown"
    ].items():

        rows.append({
            "Status": status,
            "OrderCount": values["count"],
            "Percentage": values["percentage"]
        })

    df = pd.DataFrame(rows)

    file_path = OUTPUT_DIR / "order_status.csv"

    df.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig"
    )

    print("Created:", file_path.name)


# ==================================================
# 8. RUN ALL EXPORTS
# ==================================================

def export_all_powerbi_data():

    print("\n===================================")
    print("PYTHON TO POWER BI DATA EXPORT")
    print("===================================\n")

    export_kpi_summary()
    export_monthly_revenue()
    export_product_revenue()
    export_region_revenue()
    export_order_status()

    print("\n===================================")
    print("EXPORT COMPLETED SUCCESSFULLY")
    print("===================================")

    print("\nOutput directory:")
    print(OUTPUT_DIR)


# ==================================================
# 9. MAIN
# ==================================================

if __name__ == "__main__":

    export_all_powerbi_data()