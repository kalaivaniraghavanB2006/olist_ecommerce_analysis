# Customer Support Interaction Analysis
# Beginner-friendly Python Data Analytics Project

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("==============================================")
print(" CUSTOMER SUPPORT INTERACTION ANALYSIS")
print("==============================================")

# 1. Import the raw and cleaned datasets
try:
    raw = pd.read_csv("raw_support_interactions.csv")
    tickets = pd.read_csv("clean_support_interactions.csv")

except FileNotFoundError:
    print("Dataset file not found.")
    print("Keep both CSV files in the same folder as this program.")

else:
    print("\n1. DATASET OVERVIEW")
    print("-------------------")

    print("Raw dataset shape:", raw.shape)
    print("Clean dataset shape:", tickets.shape)

    print("\nFirst five rows of cleaned data:")
    print(tickets.head())

    print("\nColumn names:")
    print(tickets.columns)

    print("\nData types:")
    print(tickets.dtypes)

    print("\nStatistical summary:")
    print(tickets.describe())

    # 2. Check the data quality before and after cleaning
    print("\n2. DATA QUALITY CHECK")
    print("---------------------")

    print("Missing values in raw data:")
    print(raw.isnull().sum())

    print("\nMissing values in cleaned data:")
    print(tickets.isnull().sum())

    print("\nDuplicate rows in raw data:", raw.duplicated().sum())
    print("Duplicate ticket IDs in raw data:",
          raw.duplicated(subset=["ticket_id"]).sum())

    print("Duplicate rows in cleaned data:", tickets.duplicated().sum())
    print("Duplicate ticket IDs in cleaned data:",
          tickets.duplicated(subset=["ticket_id"]).sum())

    print("\nRows removed during cleaning:",
          raw.shape[0] - tickets.shape[0])

    # 3. Date handling
    print("\n3. DATE ANALYSIS")
    print("---------------")

    tickets["created_at"] = pd.to_datetime(tickets["created_at"])
    tickets["Month_Number"] = tickets["created_at"].dt.month
    tickets["Weekday"] = tickets["created_at"].dt.day_name()

    print("First ticket date:", tickets["created_at"].min())
    print("Last ticket date:", tickets["created_at"].max())

    # 4. Overall support performance
    print("\n4. OVERALL SUPPORT PERFORMANCE")
    print("------------------------------")

    total_tickets = tickets["ticket_id"].count()
    total_customers = len(tickets["customer_id"].unique())
    resolved_tickets = tickets["resolved"].sum()
    unresolved_tickets = total_tickets - resolved_tickets
    resolution_rate = (resolved_tickets / total_tickets) * 100
    sla_breaches = tickets["sla_breached"].sum()
    sla_breach_rate = (sla_breaches / total_tickets) * 100

    print("Total tickets:", total_tickets)
    print("Unique customers:", total_customers)
    print("Resolved tickets:", resolved_tickets)
    print("Unresolved tickets:", unresolved_tickets)
    print("Resolution rate:", round(resolution_rate, 2), "%")
    print("SLA breached tickets:", sla_breaches)
    print("SLA breach rate:", round(sla_breach_rate, 2), "%")

    print("Average first response time:",
          round(tickets["first_response_min"].mean(), 2), "minutes")
    print("Average handling time:",
          round(tickets["handle_time_min"].mean(), 2), "minutes")
    print("Average CSAT score:",
          round(tickets["csat_score"].mean(), 2), "out of 5")

    # 5. NumPy calculations
    print("\n5. NUMPY STATISTICS")
    print("-------------------")

    response_times = tickets["first_response_min"].values
    handling_times = tickets["handle_time_min"].values

    print("Average response time:", round(np.mean(response_times), 2))
    print("Median response time:", round(np.median(response_times), 2))
    print("Response time standard deviation:", round(np.std(response_times), 2))
    print("Total response time:", round(np.sum(response_times), 2))
    print("Maximum response time:", np.max(response_times))
    print("Minimum response time:", np.min(response_times))
    print("25th percentile of response time:",
          round(np.percentile(response_times, 25), 2))
    print("75th percentile of response time:",
          round(np.percentile(response_times, 75), 2))
    print("Correlation between response and handling time:")
    print(round(np.corrcoef(response_times, handling_times)[0, 1], 2))

    # 6. Category, channel, priority and region analysis
    print("\n6. TICKET CATEGORY ANALYSIS")
    print("---------------------------")

    category_summary = tickets["category"].value_counts()
    print(category_summary)

    print("\nTop ticket categories:")
    print(category_summary.head(5))

    print("\nTickets by support channel:")
    print(tickets["channel"].value_counts())

    print("\nTickets by priority:")
    print(tickets["priority"].value_counts())

    print("\nTickets by region:")
    print(tickets["region"].value_counts())

    # 7. GroupBy analysis
    print("\n7. GROUPBY ANALYSIS")
    print("-------------------")

    print("Average response time by channel:")
    channel_summary = tickets.groupby("channel")["first_response_min"].mean()
    print(channel_summary.sort_values(ascending=False).round(2))

    print("\nAverage CSAT score by channel:")
    csat_by_channel = tickets.groupby("channel")["csat_score"].mean()
    print(csat_by_channel.sort_values(ascending=False).round(2))

    print("\nTicket count by category:")
    category_summary = tickets.groupby("category")["ticket_id"].count()
    print(category_summary.sort_values(ascending=False))

    print("\nSLA breaches by region:")
    region_sla = tickets.groupby("region")["sla_breached"].sum()
    print(region_sla.sort_values(ascending=False))

    print("\nAverage handling time by priority:")
    priority_handling = tickets.groupby("priority")["handle_time_min"].mean()
    print(priority_handling.sort_values(ascending=False).round(2))

    # 8. Filtering
    print("\n8. FILTERING TICKETS")
    print("--------------------")

    slow_responses = tickets[tickets["first_response_min"] > 30]
    print("Tickets with response time above 30 minutes:",
          slow_responses.shape[0])
    print(slow_responses[["ticket_id", "channel", "priority",
                          "first_response_min"]].head(10))

    breached_tickets = tickets[tickets["sla_breached"] == True]
    print("\nSLA breached ticket details:")
    print(breached_tickets[["ticket_id", "category", "region",
                            "first_response_min", "sla_target_min"]].head(10))

    unresolved = tickets[tickets["resolved"] == False]
    print("\nUnresolved ticket details:")
    print(unresolved[["ticket_id", "category", "priority", "channel"]].head(10))

    high_priority = tickets[
        (tickets["priority"] == "High") |
        (tickets["priority"] == "Critical")
    ]
    print("\nHigh and critical priority tickets:", high_priority.shape[0])

    # 9. Sorting
    print("\n9. SORTING")
    print("----------")

    print("Top 10 tickets with the longest handling time:")
    print(tickets.sort_values("handle_time_min", ascending=False)[
        ["ticket_id", "category", "priority", "handle_time_min"]
    ].head(10))

    print("\nTop 10 fastest first responses:")
    print(tickets.sort_values("first_response_min")[
        ["ticket_id", "channel", "first_response_min"]
    ].head(10))

    # 10. Missing-value and imputation review
    print("\n10. MISSING VALUE REVIEW")
    print("------------------------")

    print("Missing CSAT scores:", tickets["csat_score"].isnull().sum())
    print("Response times marked as imputed:",
          tickets["first_response_min_imputed"].sum())
    print("Handling times marked as imputed:",
          tickets["handle_time_min_imputed"].sum())

    # CSAT values are left missing when no survey score was provided.
    # This avoids treating an unknown score as zero.

    # 11. Monthly ticket trend
    print("\n11. MONTHLY TICKET TREND")
    print("------------------------")

    monthly_tickets = tickets.groupby("Month_Number")["ticket_id"].count()
    month_numbers = np.arange(1, 13)
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    print(monthly_tickets)

    # 12. Save analysis results
    print("\n12. SAVING RESULTS")
    print("------------------")

    tickets.to_csv("support_tickets_analysis.csv", index=False)
    category_summary.to_csv("ticket_category_summary.csv")
    channel_summary.to_csv("average_response_by_channel.csv")
    region_sla.to_csv("sla_breaches_by_region.csv")

    print("Saved: support_tickets_analysis.csv")
    print("Saved: ticket_category_summary.csv")
    print("Saved: average_response_by_channel.csv")
    print("Saved: sla_breaches_by_region.csv")

    # 13. Visualizations
    print("\n13. CREATING CHARTS")
    print("-------------------")

    # Chart 1: Monthly ticket trend
    plt.figure(figsize=(9, 5))
    plt.plot(monthly_tickets.index, monthly_tickets.values,
             color="teal", marker="o", linestyle="--")
    plt.title("Monthly Customer Support Ticket Trend", fontsize=14)
    plt.xlabel("Month")
    plt.ylabel("Number of Tickets")
    plt.xticks(month_numbers, month_names)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("monthly_ticket_trend.png")
    plt.show()
    plt.close()

    # Chart 2: Number of tickets by category
    plt.figure(figsize=(10, 5))
    bars = plt.bar(category_summary.index, category_summary.values,
                   color="skyblue", edgecolor="black")
    plt.title("Tickets by Support Category", fontsize=14)
    plt.xlabel("Ticket Category")
    plt.ylabel("Number of Tickets")
    plt.xticks(rotation=35)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.bar_label(bars, padding=3)
    plt.tight_layout()
    plt.savefig("tickets_by_category.png")
    plt.show()
    plt.close()

    # Chart 3: SLA status
    sla_counts = tickets["sla_breached"].value_counts()
    plt.figure(figsize=(7, 5))
    plt.pie(sla_counts.values,
            labels=["Within SLA", "SLA Breached"],
            autopct="%1.1f%%")
    plt.title("SLA Performance")
    plt.tight_layout()
    plt.savefig("sla_performance.png")
    plt.show()
    plt.close()

    print("Saved: monthly_ticket_trend.png")
    print("Saved: tickets_by_category.png")
    print("Saved: sla_performance.png")

    print("\n==============================================")
    print(" ANALYSIS COMPLETED SUCCESSFULLY")
    print("==============================================")
