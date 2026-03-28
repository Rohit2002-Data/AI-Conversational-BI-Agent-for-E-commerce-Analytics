import pandas as pd
import matplotlib.pyplot as plt

def generate_chart(df):
    if df is None or df.shape[1] < 2:
        return None

    x = df.columns[0]
    y = df.columns[1]

    fig, ax = plt.subplots()

    if "day" in x.lower():
        df.plot(x=x, y=y, ax=ax)
    elif len(df) <= 5:
        df.set_index(x)[y].plot(kind="pie", ax=ax)
    else:
        df.plot(kind="bar", x=x, y=y, ax=ax)

    return fig
