# Simple Linear Regression Model for Flight Tickets
This simple linear regression program retrieves data from a prompted CSV file of flight tickets and returns their R-squared, coefficients and 3D representation figures. 

It uses the following formula for the model: `Price = Intercept + Duration Coefficient * Duration + Demand Coefficient * Demand`
## Application
### Requirements
- A CSV file with the following columns: 'Airline', 'Duration', 'Total_Stops' and 'Price'.
- The currency of the prices in the CSV file.
- The duration of the flight in the format 'hh mm'.
### Output
- The R-squared value.
- The coefficients of the model.
- 3D plot of the data and the regression planes.
### Assumptions
- The price is linearly dependent on the duration and demand of the flight.
### Note
```
The program uses an open-source API to convert the prices to euros.
```

## Setup
### Requirements
- [python3](https://www.python.org/downloads/) installed
- [tkinter](https://docs.python.org/3/library/tkinter.html) installed
- [git](https://git-scm.com/downloads) installed
### Commands
Clone the repository (using https or other provided methods)
```bash
git clone https://github.com/gchatzopoulosCC/linear_regression.git
```
Create a virtual environment
```bash
python -m venv .venv
```
For Windows, the .venv should activate automatically.

For Linux, the following command has to be run:
```bash
source ./venv/bin/activate
```
Install dependencies
```bash
pip install -r requirements.txt
```
Run the program
```bash
python coef.py
```
This should be the expected output:
```git
(.venv) mycomputer$ python coef.py
HELLO!
This is a simple linear regression program that retrieves data from a prompted CSV file of flight tickets and returns their R-squared, their coefficients and a 3D representation figure.
This program uses this formula for the model: Price = Intercept + Duration Coefficient * Duration Coefficient + Demand Coefficient * Demand
Requirement: A CSV file with the following columns: 'Airline', 'Duration', and 'Price'.
Requirement: The currency of the prices in the CSV file.
Requirement: An internet connection to get the exchange rate.
Requirement: The duration of the flight in the format 'hh mm'.
Output: The R-squared value.
Output: The coefficients of the model.
Output: A 3D plot of the data and the regression plane.
Assumption: The price is linearly dependent on the duration and demand of the flight.
Note: The program uses an open-source API to convert the prices to euros.
You can exit the program at any time by prompting 'exit'.

Enter the name of the CSV file: |
```
