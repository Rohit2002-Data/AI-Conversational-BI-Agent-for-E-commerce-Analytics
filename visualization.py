import matplotlib.pyplot as plt
import pandas as pd

def generate_chart(df):
    if df is None or df.empty:
        return None

    fig, ax = plt.subplots()

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

    # 🔥 1. UNIVARIATE ANALYSIS
    if df.shape[1] == 1:
        col = df.columns[0]

        if col in numeric_cols:
            df[col].plot(kind="hist", bins=20, ax=ax)
            ax.set_title(f"Distribution of {col}")

        else:
            df[col].value_counts().plot(kind="bar", ax=ax)
            ax.set_title(f"Category Count: {col}")

        return fig

    # 🔥 2. BIVARIATE ANALYSIS
    if df.shape[1] == 2:
        x, y = df.columns

        # Numeric vs Numeric → Scatter
        if x in numeric_cols and y in numeric_cols:
            ax.scatter(df[x], df[y])
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title("Scatter Plot")

        # Category vs Numeric → Bar
        elif x in categorical_cols and y in numeric_cols:
            df.plot(kind="bar", x=x, y=y, ax=ax)
            plt.xticks(rotation=45)
            ax.set_title("Bar Chart")

        # Few categories → Pie
        elif len(df) <= 5:
            df.set_index(x)[y].plot(kind="pie", autopct="%1.1f%%", ax=ax)
            ax.set_ylabel("")
            ax.set_title("Pie Chart")

        # Time-based → Line
        elif any(k in x.lower() for k in ["day", "hour", "date"]):
            df.plot(x=x, y=y, kind="line", marker="o", ax=ax)
            ax.set_title("Time Trend")

        else:
            df.plot(x=x, y=y, kind="line", ax=ax)
            ax.set_title("Line Chart")

        return fig

    # 🔥 3. MULTIVARIATE ANALYSIS (3+ columns)

    # Case 1: Multiple numeric → correlation heatmap
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()

        im = ax.imshow(corr)
        ax.set_xticks(range(len(numeric_cols)))
        ax.set_yticks(range(len(numeric_cols)))
        ax.set_xticklabels(numeric_cols, rotation=45)
        ax.set_yticklabels(numeric_cols)

        for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")

        ax.set_title("Correlation Heatmap")
        fig.colorbar(im)

        return fig

    # Case 2: Category + multiple values → grouped bar
    if len(categorical_cols) >= 1:
        df.set_index(categorical_cols[0]).plot(kind="bar", ax=ax)
        plt.xticks(rotation=45)
        ax.set_title("Grouped Bar Chart")

        return fig

    return None
