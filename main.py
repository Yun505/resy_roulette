from flask import Flask, render_template, request, jsonify
from waitress import serve
import os
from dotenv import load_dotenv
from lambda_client import LambdaClient

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load configuration from environment variables
app.config.update(
    LAMBDA_API_URL=os.environ.get('LAMBDA_API_URL', 'http://localhost:3000')
)

# Initialize Lambda client
lambda_client = LambdaClient(app.config['LAMBDA_API_URL'])

@app.route('/')
@app.route('/index')
def index():
    """Main page - accessible to everyone"""
    return render_template('index.html')

@app.route('/retrieve', methods=['POST'])
def get_restaurant():
    """Restaurant search - accessible to everyone"""
    try:
        date = request.form['date']
        party_size = request.form['party_size']
        time = request.form['time']
        location_input = request.form['location']
        cuisines_input = request.form['cuisines']
        
        # Call Lambda API instead of local ResyRetriever
        result = lambda_client.get_restaurant(
            date=date,
            party_size=int(party_size),
            time=time,
            location=location_input,
            cuisines=cuisines_input
        )
        
        if result and result.get('success'):
            restaurant_name = result['restaurant']['name']
            return render_template('retrieve.html', title="Restaurant", restaurant=restaurant_name)
        else:
            error_message = result.get('message', 'No restaurants found.') if result else 'Failed to connect to restaurant service.'
            return render_template('retrieve.html', title="Restaurant", restaurant=error_message)
            
    except Exception as e:
        app.logger.error(f"Error in get_restaurant: {str(e)}")
        return render_template('retrieve.html', title="Restaurant", restaurant="An error occurred. Please try again.")

@app.route('/health')
def health_check():
    """Health check endpoint to verify Lambda connectivity"""
    lambda_healthy = lambda_client.health_check()
    return jsonify({
        'flask_app': 'healthy',
        'lambda_api': 'healthy' if lambda_healthy else 'unhealthy',
        'lambda_api_url': app.config['LAMBDA_API_URL']
    })

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
