# import dependencies
import pandas as pd
import numpy as np

import pyodbc
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin

# Database Setup
## Retrieve keys

import boto3
from botocore.exceptions import ClientError

def get_secret():

    secret_name = "AzureDB"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']

from Scripts.api_keys import server_name, database_name, user_name, password

## Create connection string

connection_string = "DRIVER={ODBC Driver 18 for SQL Server};SERVER={"+ server_name + "};DATABASE={" + database_name + "};UID={" + user_name + "};PWD={" + password + "}"

## Try to establish a connection

try:
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
    connection = engine.connect()

except Exception as e:
    print("Connection failed:", e)

## Save data in DF

queryEnrichedPropertyData = f"SELECT * FROM enrichedPropertyData"
queryComparisonPropertyData = f"SELECT * FROM comparisonPropertyData"
queryHistoricalPurchaseData = f"SELECT * FROM historicalPurchaseData"
queryHistoricalRentData = f"SELECT * FROM historicalRentData"

enrichedPropertyData_df = pd.read_sql(queryEnrichedPropertyData, connection)
comparisonPropertyData_df = pd.read_sql(queryComparisonPropertyData, connection)
historicalPurchaseData_df = pd.read_sql(queryHistoricalPurchaseData, connection)
historicalRentData_df = pd.read_sql(queryHistoricalRentData, connection)

## Close connection

connection.close()


# initialzie the flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# define the app 

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/enrichedPropertyData')
def get_enriched_property_data():
    
    results_list = []

    for index, row in enrichedPropertyData_df.iterrows():
        properties_dict = {
            "propertyCode": row[0],
            "propertyType": row[1],
            "description": row[2],
            "address": row[3],
            "municipality": row[4],
            "country": row[5],
            "lat": row[6],
            "lon": row[7],
            "bathrooms": row[8],
            "bedrooms": row[9],
            "size": row[10],
            "status": row[11],
            "floor": row[12],
            "hasLift": row[13],
            "newDevelopment": row[14],
            "newProperty": row[15],
            "epc": row[16],
            "purchasePrice": row[17],
            "predictedMonthlyRent": row[18],
            "URL": row[19],
            "image": row[20]
        }

        results_list.append(properties_dict)
    
    return jsonify(results_list)


@app.route('/comparisonPropertyData')
def get_comparison_property_data():
    
    results_list = []

    for index, row in comparisonPropertyData_df.iterrows():
        properties_dict = {
            "propertyCodeMain": row[0],
            "propertyCodeComp": row[1],
            "propertyType": row[2],
            "address": row[3],
            "municipality": row[4],
            "country": row[5],
            "lat": row[6],
            "lon": row[7],
            "bathrooms": row[8],
            "bedrooms": row[9],
            "size": row[10],
            "status": row[11],
            "floor": row[12],
            "hasLift": row[13],
            "newDevelopment": row[14],
            "newProperty": row[15],
            "epc": row[16],
            "monthlyRent": row[17],
            "URL": row[18],
            "image": row[19]
        }

        results_list.append(properties_dict)
    
    return jsonify(results_list)


@app.route('/historicalPurchaseData')
def get_historical_purchase_data():
    
    results_list = []

    for index, row in historicalPurchaseData_df.iterrows():
        properties_dict = {
            "city": row[0],
            "attribute": row[1],
            "date": row[2],
            "zeroBedroom": row[3],
            "oneBedroom": row[4],
            "twoBedroom": row[5],
            "threeBedroom": row[6],
            "fourBedroom": row[7],
            "fiveBedroom": row[8],
            "moreThanFiveBedroom": row[9],
            "twentyFive": row[10],
            "fifty": row[11],
            "seventyFive": row[12],
            "hundred": row[13],
            "hundredFifty": row[14],
            "twoHundred": row[15],
            "moreThanTwoHundred": row[16]
        }

        results_list.append(properties_dict)
    
    return jsonify(results_list)


@app.route('/historicalRentData')
def get_historical_rent_data():
    
    results_list = []

    for index, row in historicalRentData_df.iterrows():
        properties_dict = {
            "city": row[0],
            "attribute": row[1],
            "date": row[2],
            "zeroBedroom": row[3],
            "oneBedroom": row[4],
            "twoBedroom": row[5],
            "threeBedroom": row[6],
            "fourBedroom": row[7],
            "fiveBedroom": row[8],
            "moreThanFiveBedroom": row[9],
            "twentyFive": row[10],
            "fifty": row[11],
            "seventyFive": row[12],
            "hundred": row[13],
            "hundredFifty": row[14],
            "twoHundred": row[15],
            "moreThanTwoHundred": row[16]
        }

        results_list.append(properties_dict)
    
    return jsonify(results_list)


@app.route('/start')
def start():

    ## Input variables
    minimum_pp_input = 50000
    maximum_pp_input = 200000

    ## Filter on data

    filteredEnrichedPropertyData_df = enrichedPropertyData_df.loc[(enrichedPropertyData_df["purchasePrice"] >= minimum_pp_input) & 
                                                                  (enrichedPropertyData_df["purchasePrice"] <= maximum_pp_input), :]
    filtered_results_list = []

    for index, row in filteredEnrichedPropertyData_df.iterrows():
        properties_dict = {
            "propertyCode": row[0],
            "propertyType": row[1],
            "description": row[2],
            "address": row[3],
            "municipality": row[4],
            "country": row[5],
            "lat": row[6],
            "lon": row[7],
            "bathrooms": row[8],
            "bedrooms": row[9],
            "size": row[10],
            "status": row[11],
            "floor": row[12],
            "hasLift": row[13],
            "newDevelopment": row[14],
            "newProperty": row[15],
            "epc": row[16],
            "purchasePrice": row[17],
            "predictedMonthlyRent": row[18],
            "URL": row[19],
            "image": row[20]
        }

        filtered_results_list.append(properties_dict)
    
    return jsonify(filtered_results_list)


@app.route('/filter', methods=['POST'])
def filter():

    ## Input variables
    minimum_pp_input = float(request.form['min-price'])
    maximum_pp_input = float(request.form['max-price'])
    municipality_input = request.form['municipality']

    ## Filter on data

    filteredEnrichedPropertyData_df = enrichedPropertyData_df.loc[(enrichedPropertyData_df["purchasePrice"] >= minimum_pp_input) & 
                                                                  (enrichedPropertyData_df["purchasePrice"] <= maximum_pp_input) & 
                                                                  (enrichedPropertyData_df["municipality"] == municipality_input), :]
    filtered_results_list = []

    for index, row in filteredEnrichedPropertyData_df.iterrows():
        properties_dict = {
            "propertyCode": row[0],
            "propertyType": row[1],
            "description": row[2],
            "address": row[3],
            "municipality": row[4],
            "country": row[5],
            "lat": row[6],
            "lon": row[7],
            "bathrooms": row[8],
            "bedrooms": row[9],
            "size": row[10],
            "status": row[11],
            "floor": row[12],
            "hasLift": row[13],
            "newDevelopment": row[14],
            "newProperty": row[15],
            "epc": row[16],
            "purchasePrice": row[17],
            "predictedMonthlyRent": row[18],
            "URL": row[19],
            "image": row[20]
        }

        filtered_results_list.append(properties_dict)
    
    return jsonify(filtered_results_list)

@app.route('/startGraph')
def startGraph():

    ## Create dictionary
    start_graph_dict = {
        "purchasePrice": 200000,
        "propertyTax": 5,
        "loanToValue" : 0.7,
        "annualInterestRate": 4,
        "loanTermInYears" : 25,
        "monthlyIncome": 1000,
        "incomeTax"  : 15,
        "maintenanceCost" : 10,
        "propertyValueIncrease": 2
    }
    
    return jsonify(start_graph_dict)

@app.route('/updateGraph', methods=['POST'])
def updateGraph():

    paid_purchase_price_input = float(request.form['paid-purchase-price'])
    property_tax_input = float(request.form['property-tax'])
    ltv_input = float(request.form['ltv'])
    mortgage_rate_input = float(request.form['mortgage-rate'])
    loan_term_input = float(request.form['mortgage-tenor'])
    monthly_income_input = float(request.form['monthly-income'])
    income_tax_input = float(request.form['income-tax'])
    maintenance_input = float(request.form['maintenance'])
    property_value_increase_input = float(request.form['property-value-increase'])

    ## Create dictionary
    update_graph_dict = {
        "purchasePrice": paid_purchase_price_input,
        "propertyTax": property_tax_input,
        "loanToValue" : ltv_input,
        "annualInterestRate": mortgage_rate_input,
        "loanTermInYears" : loan_term_input,
        "monthlyIncome": monthly_income_input,
        "incomeTax"  : income_tax_input,
        "maintenanceCost" : maintenance_input,
        "propertyValueIncrease": property_value_increase_input
    }
    
    return jsonify(update_graph_dict)

@app.route('/historicalGraph')
def historicalGraph():
    return render_template('historical_graph.html')

# start the flask server
if __name__ == '__main__':
    app.run(debug=True)