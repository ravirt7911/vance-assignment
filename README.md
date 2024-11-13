# Forex Rate Visualization

## Description
This project scrapes historical exchange rates from Yahoo Finance and provides a REST API to fetch this data. A simple frontend visualizes the exchange rates over time.

## Installation

1. Clone the repository:
git clone <repository-url>
cd <repository-folder>


2. Install dependencies:
pip install -r requirements.txt
(or)
pip3 install -r requirements.txt

## Usage

1. Run the Flask application:

python app.py
(or)
python3 app.py

2. Open your web browser and navigate to:


http://localhost:5006/

## API Endpoints

### Get Forex Data

- **URL**: `/api/forex-data`
- **Method**: `POST` or `GET`
- **Query Parameters**:
 - `from`: The currency code you want to convert from (e.g., GBP).
 - `to`: The currency code you want to convert to (e.g., INR).
 - `period`: The time frame for historical data (e.g., 1M, 3M).

### Example Request



GET http://localhost:5006/api/forex-data?from=GBP&to=INR&period=1M

### Example Response


[
    {"Date": "2024-01-01", "Close": 75.0},
    {"Date": "2024-01-02", "Close": 76.0}
]

### 3. For documentation I have used swagger

http://localhost:5006/apidocs

### 3. Code Structure

**Step 1: Organize Your Files**

Create folders in your project directory to organize files better:

- Create a folder named `static` for JavaScript file.
- Create a folder named `templates` for HTML file.

Your directory structure should look like this:

your-project 
- /static # For static files (CSS, JS) --> script.js # Your JavaScript file (move here)
- /templates # For HTML templates (if using Flask's rendering) --> index.html # Your main HTML file (move here)
- app.py # Main application file
- requirements.txt # List of dependencies for easy installation
- README.md # Project documentation

**Step 2: Move Files**

Move your existing files into their respective folders:

- Move `script.js` into the `static` folder.
- Move `index.html` into the `templates` folder.

### 4. Using Requirements File

**Step 1: Create Requirements File**

Create a file named `requirements.txt` in your project directory.

**Step 2: Add Dependencies**

Open `requirements.txt` and add the following lines:

```plaintext
Flask==2.x.x          # Replace with your Flask version
yfinance==0.x.x      # Replace with your yfinance version
pandas==1.x.x        # Replace with your pandas version
apscheduler==3.x.x    # Replace with your APScheduler version
flask-cors==3.x.x     # Replace with your Flask-CORS version
flasgger==0.x.x       # Replace with your Flasgger version (if used)

