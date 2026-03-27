#!/usr/bin/env python3
"""
Static site generator to replace flask-freeze.
Renders Jinja2 templates to static HTML files.
"""

import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape

def create_url_for(current_path):
    """Create a url_for function for the current path."""
    def url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', '')
            if current_path == '/':
                return f'static/{filename}'
            else:
                return f'../static/{filename}'
        return './' if current_path == '/' else '../'
    return url_for

def build_site():
    """Build the static site."""

    # Setup directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(script_dir, 'templates')
    static_dir = os.path.join(script_dir, 'static')
    build_dir = os.path.join(script_dir, 'build')

    # Clean build directory
    if os.path.exists(build_dir):
        try:
            shutil.rmtree(build_dir)
        except:
            pass  # Directory might be in use
    os.makedirs(build_dir, exist_ok=True)

    # Setup Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    # Load projects data
    projects_path = os.path.join(static_dir, 'projects.json')
    with open(projects_path, 'r', encoding='utf-8') as f:
        projects_data = json.load(f)

    # Routes to render
    routes = [
        ('home.html', '/', {}),
        ('projects.html', '/projects/', {'projects': projects_data}),
        ('about.html', '/about/', {}),
        ('contact.html', '/contact/', {}),
    ]

    # Render templates
    for template_name, url_path, context in routes:
        # Add custom url_for function for this path
        context['url_for'] = create_url_for(url_path)
        
        template = env.get_template(template_name)
        html_content = template.render(**context)

        # Create output path
        if url_path == '/':
            output_path = os.path.join(build_dir, 'index.html')
        else:
            # Remove leading/trailing slashes and create directory structure
            path_parts = url_path.strip('/').split('/')
            output_dir = os.path.join(build_dir, *path_parts)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, 'index.html')

        # Write HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    # Copy static files
    static_build_dir = os.path.join(build_dir, 'static')
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, static_build_dir)

    # Copy CNAME if it exists
    cname_path = os.path.join(script_dir, 'CNAME')
    if os.path.exists(cname_path):
        shutil.copy2(cname_path, build_dir)

    print("Static site built successfully!")

if __name__ == '__main__':
    build_site()