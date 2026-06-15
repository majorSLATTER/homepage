from flask import Flask, render_template, request
import json
import os
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/projects/')
def projects():
    # Load projects from JSON file
    projects_path = os.path.join(app.root_path, 'static', 'projects.json')
    with open(projects_path, 'r', encoding='utf-8') as f:
        projects_data = json.load(f)
    return render_template('projects.html', projects=projects_data)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/afbudsrejser/')
def afbudsrejser():
    countries = ['ES', 'PT', 'IT', 'GR', 'FR', 'MT']
    results_by_country = {}
    max_price = int(request.args.get('max_price', 8000))
    
    try:
        url = 'https://www.afbudsrejser.dk/services/charter/api_search'
        base_params = {
            'category': 'SUNBATH',
            'board_type': 'all_inclusive',
            'adults': 2,
            'max_price': max_price,
            'depart_date_min': '2026-07-06T00:00:00Z',
            'depart_date_max': '2026-07-19T23:59:59Z',
            'days_min': 5,
            'days_max': 7,
            'limit': 25,
            'sort': 'price_asc',
            'fields': ['hotel_name', 'destination_name', 'country_name', 'departure_date', 'return_date', 'price_per_pers', 'url']
        }
        
        for country in countries:
            try:
                params = {**base_params, 'country_iso': country}
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    results_by_country[country] = response.json().get('results', [])
                else:
                    results_by_country[country] = []
            except Exception as e:
                results_by_country[country] = []
    except Exception as e:
        results_by_country = {country: [] for country in countries}
    
    return render_template('afbudsrejser.html', results_by_country=results_by_country, max_price=max_price)

if __name__ == '__main__':
    app.run(debug=True)