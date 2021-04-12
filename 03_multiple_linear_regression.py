from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.metrics import r2_score
import pickle


def multiple_linear_regression():
    """This function performs the multiple linear regression and exports a machine learning model for use in a
    production system."""

    """TO DO ITEMS:
    1. check for multicolinearity (VIF)
    2. interactions?
    3. check that assumptions for linear regression are met"""

    # load data sets
    response = pd.read_csv("data/response.csv")
    #df = pd.read_csv("data/explanatory.csv")
    df = pd.read_csv("data/explanatory_subset.csv")

    # split data into training and test datasets
    X_train, X_test, y_train, y_test = train_test_split(df, response, test_size=0.3, random_state=11556)

    # create linear model
    model = LinearRegression()

    # fit the model to the training data
    model.fit(X_train, y_train)

    # make predictions on the test dataset
    predictions = model.predict(X_test)

    # see how good predictions are using adjusted r^2 value
    r2 = r2_score(y_test, predictions)
    num_pred = df.shape[1]
    adj_r2 = 1 - (1 - r2) * (df.shape[0] - 1) / (df.shape[0] - num_pred - 1)
    print(adj_r2)

    # export initial model
    with open("model_subset.pkl", "wb") as model_file:
        pickle.dump(model, model_file)

def main():
    multiple_linear_regression()

if __name__ == "__main__":
    main()