from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/projects')
def projects():
    # Load projects from JSON file
    projects_path = os.path.join(app.root_path, 'static', 'projects.json')
    with open(projects_path, 'r') as f:
        projects_data = json.load(f)
    return render_template('projects.html', projects=projects_data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')