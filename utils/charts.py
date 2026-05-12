import matplotlib.pyplot as plt
from database import db
from collections import defaultdict
from datetime import datetime, timedelta

# ================= MAIN BAR CHART =================

def get_chart_figure(user_id):

    data = db.get_expenses(user_id)

    if not data:
        return None

    categories = {}

    for row in data:
        categories[row[3]] = categories.get(row[3], 0) + float(row[4])

    labels = list(categories.keys())
    values = list(categories.values())

    fig = plt.Figure(figsize=(7,4), dpi=100)
    ax = fig.add_subplot(111)

    colors = ["#4CAF50",
              "#2196F3",
              "#FF9800",
              "#9C27B0",
              "#F44336",
              "#009688"]

    bars = ax.bar(labels,
                  values,
                  color=colors[:len(labels)])

    ax.set_title("Expense Overview",
                 fontsize=14,
                 weight="bold")

    ax.grid(axis='y',
            linestyle='--',
            alpha=0.5)

    ax.tick_params(axis='x',
                   rotation=20)

    for bar in bars:

        h = bar.get_height()

        ax.text(bar.get_x() + bar.get_width()/2,
                h,
                f"₹ {int(h)}",
                ha='center',
                va='bottom',
                fontsize=9)

    fig.tight_layout()

    return fig

# ================= POPUP BAR CHART =================

def show_chart(user_id):

    fig = get_chart_figure(user_id)

    if fig:
        plt.figure(fig.number)
        plt.show()

# ================= MONTHLY CHART =================

def show_monthly_chart(user_id):

    data = db.get_expenses(user_id)

    if not data:
        return

    monthly = defaultdict(float)

    for row in data:

        month = row[2][:7]

        monthly[month] += float(row[4])

    months = sorted(monthly.keys())
    values = [monthly[m] for m in months]

    fig = plt.figure(figsize=(9,5))

    ax = fig.add_subplot(111)

    bars = ax.bar(months,
                  values,
                  color="#673AB7")

    ax.set_title("Monthly Expenses",
                 fontsize=14,
                 weight="bold")

    ax.grid(axis='y',
            linestyle='--',
            alpha=0.5)

    for bar in bars:

        h = bar.get_height()

        ax.text(bar.get_x() + bar.get_width()/2,
                h,
                f"₹ {int(h)}",
                ha='center',
                va='bottom')

    plt.xticks(rotation=25)

    plt.tight_layout()

    plt.show()

# ================= LAST 7 DAYS =================

def show_last7days_chart(user_id):

    data = db.get_expenses(user_id)

    last7 = {}

    today = datetime.today()

    for i in range(7):

        day = (today - timedelta(days=i)).strftime("%Y-%m-%d")

        last7[day] = 0

    for row in data:

        if row[2] in last7:

            last7[row[2]] += float(row[4])

    days = list(last7.keys())[::-1]
    values = list(last7.values())[::-1]

    fig = plt.figure(figsize=(9,5))

    ax = fig.add_subplot(111)

    bars = ax.bar(days,
                  values,
                  color="#795548")

    ax.set_title("Last 7 Days Expenses",
                 fontsize=14,
                 weight="bold")

    ax.grid(axis='y',
            linestyle='--',
            alpha=0.5)

    for bar in bars:

        h = bar.get_height()

        ax.text(bar.get_x() + bar.get_width()/2,
                h,
                f"₹ {int(h)}",
                ha='center',
                va='bottom')

    plt.xticks(rotation=25)

    plt.tight_layout()

    plt.show()