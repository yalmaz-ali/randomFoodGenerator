import requests
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

meals = {
    'Fast Food': {
        'Chicken': [
            ('Chicken Burger', 380),
            ('Grill Burger', 450),
            ('Pizza', 500),
        ],
        'Beef': [
            ('Beef Burger', 400),
        ],
        'Vegetarian': [
            ('Veggie Pizza', 450),
            ('Falafel Wrap', 350),
        ]
    },
    'Chinese': {
        'Chicken': [
            ('Kung Pao Chicken + Rice', 800),
            ('Sweet and Sour Chicken + Rice', 750),
        ],
        'Beef': [
            ('Beef Noodles', 700),
            ('Beef with Broccoli + Rice', 850),
        ],
        'Vegetarian': [
            ('Vegetable Stir-fry + Rice', 600),
            ('Spring Rolls', 500),
        ]
    },
    'Desi': {
        'Chicken': [
            ('Chicken Biryani', 300),
            ('Chicken Karahi', 1000),
        ],
        'Beef': [
            ('Beef Nihari', 900),
            ('Nalli Pulao', 1200),
            ('Chapli Kebab', 200),
        ],
        'Vegetarian': [
            ('Dal Tadka', 250),
            ('Vegetable Curry', 200),
        ]
    }
}

# Pixabay API Integration
def fetch_food_image(query):
    API_KEY = '45964479-594e006215b34532959ca205b'  # Replace this with your actual Pixabay API key
    url = f'https://pixabay.com/api/?key={API_KEY}&q={query}&image_type=photo&category=food'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['hits']:
            return data['hits'][0]['webformatURL']  # Fetching the first image result
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_meal', methods=['POST'])
def get_meal():
    category = request.form.get('category')
    taste = request.form.get('taste')
    budget = float(request.form.get('budget')) if request.form.get('budget') else None

    if category and taste and budget:
        # Filter meals based on budget
        available_meals = [(meal, price) for meal, price in meals[category][taste] if price <= budget]

        if available_meals:
            meal, price = random.choice(available_meals)

            # Fetch image for the selected meal
            image_url = fetch_food_image(meal)

            return jsonify({'meal': f"{meal} (PKR {price})", 'image_url': image_url})
        else:
            return jsonify({'error': 'No meals found within the selected budget.'}), 400
    else:
        return jsonify({'error': 'Please select category, taste, and enter a budget.'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
