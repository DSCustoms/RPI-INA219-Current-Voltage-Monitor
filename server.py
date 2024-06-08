from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# Route to display the index.html page
@app.route('/')
def index():
    # Get the absolute path to sensor_data.txt
    data_file_path = os.path.join(os.path.dirname(__file__), 'sensor_data.txt')

    # Read sensor data from the file
    if os.path.exists(data_file_path):
        with open(data_file_path, 'r') as file:
            sensor_data = [line.strip().split(',') for line in file]
    else:
        sensor_data = []

    # Pass sensor data to the template for rendering
    return render_template('index.html', sensor_data=sensor_data)

# Route to reset sensor data
@app.route('/reset', methods=['POST'])
def reset_data():
    try:
        # Get the absolute path to sensor_data.txt
        data_file_path = os.path.join(os.path.dirname(__file__), 'sensor_data.txt')

        # Erase the contents of the file
        with open(data_file_path, 'w') as file:
            file.write('')

        return jsonify(success=True)
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error to the console
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
