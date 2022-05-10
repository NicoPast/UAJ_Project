import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import plotly.express as px


def main():
    print("Hello World!")
    plt.plot(np.arange(50), np.random.rand(50))
    plt.show()

    fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
    # fig.write_html('first_figure.html', auto_open=True)
    fig.show()

    # df["VALOR_CUANTILES"] = pd.qcut(df.VALOR_MEDIANO, 5)
    # df.boxplot(column="INDICE_CRIMEN", by="VALOR_CUANTILES",
	# figsize=(8,6))
    # plt.show()

if __name__ == "__main__":
    main()