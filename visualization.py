import matplotlib.pyplot as plt

def generate_chart(df):
    if df is None or df.empty or df.shape[1] < 2:
        return None

    x = df.columns[0]
    y = df.columns[1]

    fig, ax = plt.subplots()

    if "hour" in x.lower() or "day" in x.lower():
        df.plot(x=x, y=y, kind="line", marker="o", ax=ax)

    elif len(df) <= 5:
        df.set_index(x)[y].plot(kind="pie", autopct="%1.1f%%", ax=ax)

    else:
        df.plot(kind="bar", x=x, y=y, ax=ax)
        plt.xticks(rotation=45)

    plt.tight_layout()
    return fig
