from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load the Excel file
df = pd.read_csv('Book1.csv', dtype={'ZIP CODE': str, '10': float, '15': float, '20': float, '25': float})  # Ensure ZIP codes are read as strings

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    # Retrieve parameters from the query string
    zip_code = request.args.get('zipCode')
    radius_column = request.args.get('radiusColumn')

    # Validate radius_column to ensure it's one of the expected values
    if radius_column not in ['10', '15', '20', '25']:
        return jsonify({'error': 'Invalid radius column'}), 400

    # Find the row with the matching ZIP code
    row = df[df['ZIP CODE'] == zip_code]
    if row.empty:
        return jsonify({'error': 'No data found for the given ZIP code'}), 404

    # Return the value from the specified column
    result = row.iloc[0][radius_column]
    return jsonify({radius_column: result})

# if __name__ == '__main__':
#     app.run(debug=True)
