from flask import Flask, render_template, request, jsonify
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
    # Route is only used for local development
    # In production (GitHub Pages), this page uses client-side JavaScript to fetch API data
    return render_template('afbudsrejser.html')

@app.route('/api/charter-search')
def charter_search():
    """Proxy endpoint for charter API to handle CORS issues"""
    try:
        # Get query parameters from client
        country_iso = request.args.get('country_iso')
        if not country_iso:
            return jsonify({'error': 'country_iso parameter required'}), 400
        
        # Build the external API URL
        api_url = 'https://www.afbudsrejser.dk/services/charter/api_search'
        
        params = {
            'country_iso': country_iso,
            'category': request.args.get('category', 'SUNBATH'),
            'board_type': request.args.get('board_type', 'all_inclusive'),
            'adults': request.args.get('adults', 2),
            'max_price': request.args.get('max_price', 8000),
            'depart_date_min': request.args.get('depart_date_min'),
            'depart_date_max': request.args.get('depart_date_max'),
            'days_min': request.args.get('days_min', 5),
            'days_max': request.args.get('days_max', 7),
            'limit': request.args.get('limit', 25),
            'sort': request.args.get('sort', 'price_asc')
        }
        
        # Add fields parameter (can be multiple)
        fields = request.args.getlist('fields')
        if fields:
            params['fields'] = fields
        
        # Fetch from external API
        response = requests.get(api_url, params=params, timeout=10)
        
        # Return the response as JSON
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'results': []}), 200
            
    except Exception as e:
        return jsonify({'error': str(e), 'results': []}), 500

if __name__ == '__main__':
    app.run(debug=True)