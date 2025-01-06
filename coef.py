import re
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import numpy as np


# Helpers
def convert_to_minutes(time):
    """Converts a time in the format 'hh mm' to minutes."""
    parts = time.split(" ")
    if len(parts) == 2:
        h, m = parts
    elif len(parts) == 1:
        h, m = parts[0], "0m"
    else:
        raise ValueError(f"Unexpected time format: {time}")

    # Remove the 'h' and 'm' characters
    h = re.sub(r"\D", "", h)
    m = re.sub(r"\D", "", m)
    return int(h) * 60 + int(m)


def get_exchange_rate():
    api_response = requests.get(
        "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/eur.json"
    )
    exchange_rate = api_response.json()
    return exchange_rate


def convert_to_euro(amount, currency, exchange_rate=None):
    # Use an open-source API to convert a given amount of a currency to euros.
    if exchange_rate is None:
        raise ValueError("Exchange rate not provided.")
    exchange_rate = exchange_rate["eur"][currency]
    return amount / exchange_rate


def display_model(model, data, y):
    # Plot the data
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(data["Duration"], data["Demand"], y, color="blue")
    ax.set_xlabel("Duration")
    ax.set_ylabel("Demand")
    ax.set_zlabel("Price (in euros)")
    ax.set_title("Price vs Duration vs Demand")

    # Plot the regression plane
    xx, yy = np.meshgrid(
        np.linspace(data["Duration"].min(), data["Duration"].max(), 100),
        np.linspace(data["Demand"].min(), data["Demand"].max(), 100),
    )
    zz = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.plot_surface(xx, yy, zz, color="red", alpha=0.5)

    plt.show()


def intro():
    print("HELLO!")
    print(
        "This is a simple linear regression program that retrieves data from a prompted CSV file of flight tickets and returns their R-squared, their coefficients and a 3D representation figure."
    )
    print(
        "This program uses this formula for the model: Price = Intercept + Duration Coefficient * Duration Coefficient + Demand Coefficient * Demand"
    )
    print(
        "Requirement: A CSV file with the following columns: 'Airline', 'Duration', and 'Price'."
    )
    print("Requirement: The currency of the prices in the CSV file.")
    print("Requirement: An internet connection to get the exchange rate.")
    print("Requirement: The duration of the flight in the format 'hh mm'.")
    print("Output: The R-squared value.")
    print("Output: The coefficients of the model.")
    print("Output: A 3D plot of the data and the regression plane.")
    print(
        "Assumption: The price is linearly dependent on the duration and demand of the flight."
    )
    print("Note: The program uses an open-source API to convert the prices to euros.")
    print("You can exit the program at any time by prompting 'exit'.")
    print()


# Main function
def main():
    # Introduction
    intro()

    # Get the data from a CSV file
    file = input("Enter the name of the CSV file: ")
    try:
        if file == "exit":
            return 0
        data = pd.read_csv(file)
    except FileNotFoundError:
        print(f"File {file} not found.")
        return 1

    # Get the currency of the prices
    currency = input("Enter the currency of the prices: ")
    if currency == "exit":
        return 0

    # Get the exchange rate
    exchange_rate = get_exchange_rate()

    if currency not in exchange_rate["eur"]:
        print(f"Currency {currency} not supported.")
        return 1

    # Get the demand of each company
    data["Duration"] = data["Duration"].apply(convert_to_minutes)
    data["Demand"] = data["Airline"].map(data["Airline"].value_counts())

    # Get the independent and dependent variables
    X = data[["Duration", "Demand"]]
    y = data["Price"].apply(
        convert_to_euro, currency=currency, exchange_rate=exchange_rate
    )

    # Train the model
    model = LinearRegression()
    model.fit(X, y)

    # Get r-squared
    r_squared = model.score(X, y)
    print(f"R-squared: {r_squared}")

    # Get the coefficients
    duration_coef, demand_coef = model.coef_
    print(f"Duration coefficient: {duration_coef}")
    print(f"Demand coefficient: {demand_coef}")
    print(f"Intercept: {model.intercept_}")

    display_model(model, data, y)


# Run the main function
if __name__ == "__main__":
    main()
