import pandas as pd
import numpy as np
import datetime
import os


def initial_data_cleaning():
    """This function will be used to process the initial dataset. Outliers have been removed, specifically homes with a
    Year_Built date of 0, homes with a price less than 10,000 or greater than 5,000,000. Categorical variables have been
    converted to dummy variables (binary yes/no) with a single variable being dropped. Imported data needs to be
    converted from .xlsx to .csv before processing. Data originally comes from
    http://services.wakegov.com/realdata_extracts/RealEstData04072021.xlsx"""
    # load data, specific columns were chosen before this preprocessing step after looking at the data dictionary
    cols = [20, 21, 22, 29, 31, 37, 40, 41, 46, 48, 62, 64, 66, 76, 86]
    df = pd.read_csv("data/RealEstData04042021.csv", usecols=cols)

    # clean up data, remove rows with missing values
    df = df.dropna()

    # 3 homes have a year of 0, causing some problems down the road (will drop for now)
    df = df[df["Year_Built"] != 0]

    # we only want homes for individuals not corporations or public entities
    df = df[df["BILLING_CLASS"] == 2]
    df = df.drop(columns=["BILLING_CLASS"])

    # drop all rows where Total_sale_Price == 0
    df = df[df["Total_sale_Price"] != "0"]

    # convert Total_sale_Price to numeric, remove outliers that will impact analysis (no values less than
    # 10,000 or greater than 5,000,000
    df["Total_sale_Price"] = df["Total_sale_Price"].str.replace(",", "").astype(int)
    df = df[df["Total_sale_Price"] > 9999]
    df = df[df["Total_sale_Price"] < 5000001]

    # drop all rows that have Land_classification that is not in ("R", "N", "B", "H", "G")
    land_class = ["R", "N", "B", "H", "G"]
    df = df[df["Land_classification"].isin(land_class)]

    # user unlikely to know this variable, will drop for now
    df = df.drop(columns=["Land_classification"])

    # specify homes that have a sale by dates that is after january 1, 2015
    df["Total_Sale_Date"] = pd.to_datetime(df["Total_Sale_Date"], format="%m/%d/%Y")
    houses_date = datetime.datetime(2015, 1, 1)
    df = df[df["Total_Sale_Date"] >= houses_date]
    df = df.drop(columns=["Total_Sale_Date"])

    # utilities variable seems messy. lets make two new columns binary for gas and electric
    conditions = [(df["UTILITIES"] == "ALL"), (df["UTILITIES"] == "WGE"), (df["UTILITIES"] == "GE"),
                  (df["UTILITIES"] == "SGE"), (df["UTILITIES"] == "WSG"), (df["UTILITIES"] == "WG"),
                  (df["UTILITIES"] == "G"), (df["UTILITIES"] == "SG")]
    choices = [1, 1, 1, 1, 1, 1, 1, 1]
    df["gas"] = np.select(conditions, choices)

    conditions = [df["UTILITIES"] == "ALL", df["UTILITIES"] == "E", df["UTILITIES"] == "WSE", df["UTILITIES"] == "WE",
                  df["UTILITIES"] == "WGE", df["UTILITIES"] == "GE", df["UTILITIES"] == "SGE", df["UTILITIES"] == "SE"]
    choices = [1, 1, 1, 1, 1, 1, 1, 1]
    df["electric"] = np.select(conditions, choices)

    df = df.drop(columns=["UTILITIES"])

    # lots of 0's for Remodeled_Year, lets change this to a binary remodeled yes no column
    df["remodeled"] = np.where(df["Remodeled_Year"] != 0, 1, 0)
    df = df.drop(columns=["Remodeled_Year"])

    # story_height needs consolidation of variables, A= 1 story, C = 2 story, other = all other options
    df["Story_Height"] = df["Story_Height"].replace(["B", "I", "L", "K", "J", "E", "D", "M", "N", "O"], "other")

    # story_height is categorical, replace with dummy variables. A is the default (single story home)
    story_height = pd.get_dummies(df["Story_Height"], drop_first=True, prefix="story")

    # drop original Story_Height variable and add dummy variables
    df = df.drop(columns=["Story_Height"])
    df = pd.concat([df, story_height], axis=1)

    # variable HEAT is overwhelmingly forced air (A). will drop for now
    df = df.drop(columns=["HEAT"])

    # variable AIR is very homogenous, will drop for now
    df = df.drop(columns=["AIR"])

    # bath looks like a great variable, need to dummy encode, default is A (one bath)
    bath = pd.get_dummies(df["BATH"], drop_first=True, prefix="bath")

    # drop original BATH variable and add dummy variables
    df = df.drop(columns=["BATH"])
    df = pd.concat([df, bath], axis=1)

    # physical_zip_code likely a good variable, need to dummy_encode, default is missing zip (zip = 0??)
    zip_codes = pd.get_dummies(df["PHYSICAL_ZIP_CODE"].astype(int), prefix="zip")
    df = df.drop(columns=["PHYSICAL_ZIP_CODE"])
    df = pd.concat([df, zip_codes], axis=1)

    # separate the response variable from the explanatory variables
    response = df["Total_sale_Price"]

    df.drop(columns=["Total_sale_Price"], inplace=True)

    os.chdir("data")

    response.to_csv("response.csv", index=False)
    df.to_csv("explanatory.csv", index=False)


def main():
    initial_data_cleaning()


if __name__ == "__main__":
    main()
