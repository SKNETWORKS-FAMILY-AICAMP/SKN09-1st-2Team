import matplotlib.pyplot as plt

def plot_monthly_trends(monthly_sales, title="Monthly Trends"):
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_sales.sum(axis=0).plot(kind="line", marker='o', ax=ax)
    ax.set_title(title, fontsize=14)
    ax.set_ylabel("Demand (Units)", fontsize=12)
    ax.set_xlabel("Month", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig