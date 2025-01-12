import re
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
import numpy as np


# Helpers
def convert_stops(stops):
    # Consider NAN values
    if pd.isna(stops):
        return np.nan
    if stops == "non-stop":
        return 0
    # Get the number of stops from the string
    match = re.search(r"\d+", stops)
    if match:
        return int(match.group())
    else:
        raise ValueError(f"Unexpected stops format: {stops}")

def convert_to_minutes(time):
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
    # Plot Distance vs Stops vs Price
    fig = plt.figure(figsize=(15, 5))
    ax = fig.add_subplot(131, projection='3d')
    ax.scatter(data["Distance"], data["Stops"], y, color="blue")
    ax.set_xlabel("Distance")
    ax.set_ylabel("Stops")
    ax.set_zlabel("Price (in euros)")
    ax.set_title("Price vs Distance vs Stops")

    xx, yy = np.meshgrid(np.linspace(data["Distance"].min(), data["Distance"].max(), 100),
                         np.linspace(data["Stops"].min(), data["Stops"].max(), 100))
    zz = model.predict(np.c_[xx.ravel(), yy.ravel(), np.full(xx.ravel().shape, data["Demand"].mean())]).reshape(xx.shape)
    ax.plot_surface(xx, yy, zz, color='red', alpha=0.5)

    # Plot Distance vs Demand vs Price
    ax = fig.add_subplot(132, projection='3d')
    ax.scatter(data["Distance"], data["Demand"], y, color="blue")
    ax.set_xlabel("Distance")
    ax.set_ylabel("Demand")
    ax.set_zlabel("Price (in euros)")
    ax.set_title("Price vs Distance vs Demand")

    xx, yy = np.meshgrid(np.linspace(data["Distance"].min(), data["Distance"].max(), 100),
                         np.linspace(data["Demand"].min(), data["Demand"].max(), 100))
    zz = model.predict(np.c_[xx.ravel(), np.full(xx.ravel().shape, data["Stops"].mean()), yy.ravel()]).reshape(xx.shape)
    ax.plot_surface(xx, yy, zz, color='red', alpha=0.5)

    # Plot Stops vs Demand vs Price
    ax = fig.add_subplot(133, projection='3d')
    ax.scatter(data["Stops"], data["Demand"], y, color="blue")
    ax.set_xlabel("Stops")
    ax.set_ylabel("Demand")
    ax.set_zlabel("Price (in euros)")
    ax.set_title("Price vs Stops vs Demand")

    xx, yy = np.meshgrid(np.linspace(data["Stops"].min(), data["Stops"].max(), 100),
                         np.linspace(data["Demand"].min(), data["Demand"].max(), 100))
    zz = model.predict(np.c_[np.full(xx.ravel().shape, data["Distance"].mean()), xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.plot_surface(xx, yy, zz, color='red', alpha=0.5)

    plt.show()


def get_latitude(airport, airport_coords):
    return airport_coords.get(airport, (np.nan, np.nan))[0]

def get_longitude(airport, airport_coords):
    return airport_coords.get(airport, (np.nan, np.nan))[1]


def get_distance(route, airport_coords):
    from geopy.distance import geodesic

    if pd.isna(route):
        return np.nan

    # Get all the airports from the route
    airports = route.split(" ? ")
    if len(airports) < 2:
        raise ValueError(f"Unexpected route format: {route}")
    
    # Get the coordinates of the airports
    coordinates = [(get_latitude(airport, airport_coords), get_longitude(airport, airport_coords)) for airport in airports]
    
    # Get the distance between the airports
    distance = geodesic(*coordinates).kilometers
    return distance
    


def intro():
    print("HELLO!")
    print(
        "This is a simple linear regression program that retrieves data from a prompted CSV file of flight tickets and returns their R-squared, their coefficients and a 3D representation figure."
    )
    print(
        "This program uses this formula for the model: Price = Intercept + Distance Coefficient * Distance Coefficient + Stops Coefficient * Stops + Demand Coefficient * Demand"
    )
    print(
        "Requirement: A CSV file with the following columns: 'Airline', 'Route', 'Total_Stops', and 'Price'."
    )
    print("Requirement: The currency of the prices in the CSV file.")
    print("Requirement: An internet connection to get the exchange rate.")
    print("Requirement: The Route of the flight in the format 'IATA ? IATA ? ... ? IATA'")
    print("Output: The R-squared value.")
    print("Output: The coefficients of the model.")
    print("Output: 3D plots of the data and the regression planes.")
    print(
        "Assumption: The price is linearly dependent on the Distance and demand of the flight."
    )
    print("Note: The program uses an open-source API to convert the prices to euros.")
    print("You can exit the program at any time by prompting 'exit'.")
    print()


# Main function
def main():
    ## Introduction
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
#
    # Get the exchange rate
    exchange_rate = get_exchange_rate()

    if currency not in exchange_rate["eur"]:
        print(f"Currency {currency} not supported.")
        return 1
    
    # Data
    data = pd.read_csv("Data_Train.csv")

    # Convert stops
    data["Stops"] = data["Total_Stops"].apply(convert_stops)
    
    # Calculate the distance between the airports
    airport_data = pd.read_csv("airports.csv")
    airport_coords = {
        row["IATA"]: (row["Latitude"], row["Longitude"])
        for _, row in airport_data.iterrows()
    }
    data["Distance"] = data["Route"].apply(lambda route: get_distance(route, airport_coords))

    # Drop NaN values
    data = data.dropna()

    # Get the appropriate columns
    data["Demand"] = data["Airline"].map(data["Airline"].value_counts())

    # Fill NaN values with 0 and convert to integers
    data["Stops"] = data["Stops"].fillna(0).astype(int)

    # Get the independent and dependent variables
    X = data[["Distance", "Stops", "Demand"]]
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
    Distance_coef, stops_coef, demand_coef = model.coef_
    print(f"Intercept: {model.intercept_}")
    print(f"Distance coefficient: {Distance_coef}")
    print(f"Stops coefficient: {stops_coef}")
    print(f"Demand coefficient: {demand_coef}")

    display_model(model, data, y)


# Run the main function
if __name__ == "__main__":
    main()
