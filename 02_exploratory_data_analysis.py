import pandas as pd
import matplotlib.pyplot as plt
import os


def eta():
    """This function creates graphs of all explanatory variables vs the response variables. This can be used to identify
    if relationships are linear or not."""
    os.chdir("data")

    df = pd.read_csv("explanatory.csv")
    response = pd.read_csv("response.csv")

    os.chdir("../images")
    for col in df.columns:
        print(col)
        file_name = col + ".png"
        plt.scatter(y=response["Total_sale_Price"], x=df[col])
        plt.savefig(file_name)
        plt.clf()


def main():
    eta()


if __name__ == "__main__":
    main()
