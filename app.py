from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
from xgboost import XGBRegressor

app = Flask(__name__)

# Load the trained model
model = joblib.load('model.pkl')

# Sample columns list, adjust as per your final model's expected input features
columns = ['day', 'month', 'year', 'city_Delhi', 'city_Kolkata', 'city_Mumbai', 'fuel_type_Diesel']

def predict_fuel_price(day, month, year, city, fuel_type):
    # Prepare the input data in the format expected by the model
    input_data = {
        'day': [day],
        'month': [month],
        'year': [year]
    }
    
    for col in columns:
        if col not in input_data:
            input_data[col] = [1] if col == f'city_{city}' or col == f'fuel_type_{fuel_type}' else [0]

    input_df = pd.DataFrame(input_data)
    
    # Make the prediction using the trained model
    predicted_price = model.predict(input_df)
    return predicted_price[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    day = data['day']
    month = data['month']
    year = data['year']
    city = data['city']
    fuel_type = data['fuelType']
    
    predicted_price = predict_fuel_price(day, month, year, city, fuel_type)
    
    return jsonify({'predicted_price': predicted_price})

if __name__ == '__main__':
    app.run(debug=True)