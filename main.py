from flask import Flask, render_template, request
from waitress import serve
import retrieve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/retrieve', methods=['POST'])
def get_restaurant():
    date = request.form['date']
    party_size = request.form['party_size']
    time = request.form['time']
    location_input = request.form['location']
    cuisines_input = request.form['cuisines']
    
    location = retrieve.get_location(location_input)
    cuisines_list = [cuisine.strip().lower() for cuisine in cuisines_input.split(',')]
    
    restaurants = retrieve.get_restaurants(date, party_size, time, location, cuisines_list)
    
    if restaurants:
        restaurant_name = restaurants[0]['name']
        return render_template('retrieve.html', title="Restaurant", restaurant=restaurant_name)
    else:
        return render_template('retrieve.html', title="Restaurant", restaurant="No restaurants found.")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
