# consumes the backlog api using the requests library
# and returns the response
# uses api_key to authenticate
# the api_key is stored in the environment variable API_KEY and is accessed using os.getenv
# the api_key is passed as a header in the request

import os
import requests

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BACKLOG_URL')

def get_headers():
    """Returns the headers required for the API requests."""
    return {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

def create_diagram(name, definition):
    """Creates a new diagram with the given name and definition."""
    url = f"{BASE_URL}/diagrams"
    payload = {
        "name": name,
        "definition": definition
    }
    response = requests.post(url, headers=get_headers(), json=payload)
    return response.json()

def get_list_diagrams():
    """Retrieves the list of all diagrams."""
    url = f"{BASE_URL}/diagrams"
    response = requests.get(url, headers=get_headers())
    return response.json()

def update_diagram_graphic(diagram_name, updates):
    """Updates the graphic of a specific diagram identified by its name."""
    url = f"{BASE_URL}/diagram/update-graphic/{diagram_name}"
    response = requests.patch(url, headers=get_headers(), json=updates)
    return response.json()

def update_diagram(id, updates):
    """Updates a specific diagram identified by its ID."""
    url = f"{BASE_URL}/diagrams/{id}"
    response = requests.patch(url, headers=get_headers(), json=updates)
    return response.json()

def get_png_diagram(diagram_name):
    """Retrieves the PNG image of a specific diagram identified by its name."""
    url = f"{BASE_URL}/diagram/png/{diagram_name}"
    response = requests.get(url, headers=get_headers())
    return response.content

def get_plant_url_diagram(diagram_name):
    """Retrieves the PlantUML URL of a specific diagram identified by its name."""
    url = f"{BASE_URL}/diagram/plant-url/{diagram_name}"
    response = requests.get(url, headers=get_headers())
    return response.json()

def get_diagram(id):
    """Retrieves a specific diagram identified by its ID."""
    url = f"{BASE_URL}/diagram/{id}"
    response = requests.get(url, headers=get_headers())
    return response.json()

def get_list_projects():
    """Retrieves the list of all projects."""
    url = f"{BASE_URL}/project-command/all"
    response = requests.get(url, headers=get_headers())
    return response.json()

def get_projects_tree(project):
    """Retrieves the project tree for a specific project."""
    url = f"{BASE_URL}/project-command/{project}/tree"
    response = requests.get(url, headers=get_headers())
    return response.json()

def get_list_feature_types():
    """Retrieves the list of all feature types."""
    url = f"{BASE_URL}/featuretypes"
    response = requests.get(url, headers=get_headers())
    return response.json()

def create_project(name, code, clientName=None, description=None):
    """Creates a new project with the given details."""
    url = f"{BASE_URL}/projects"
    payload = {
        "name": name,
        "code": code,
        "clientName": clientName,
        "description": description
    }
    response = requests.post(url, headers=get_headers(), json=payload)
    return response.json()

def get_story_tree(storyID):
    """Retrieves the story tree for a specific story identified by its ID."""
    url = f"{BASE_URL}/story-command/{storyID}/tree"
    response = requests.get(url, headers=get_headers())
    return response.json()

def update_story(story_data):
    """Updates a story with the given data."""
    url = f"{BASE_URL}/story-command/update"
    response = requests.post(url, headers=get_headers(), json=story_data)
    return response.json()

def refresh_feature_types():
    """Refreshes the list of feature types."""
    url = f"{BASE_URL}/feature-command/refresh-types"
    response = requests.get(url, headers=get_headers())
    return response.json()

def add_feature_to_story(story, feature_data):
    """Adds a feature to a specific story."""
    url = f"{BASE_URL}/feature-command/{story}/add"
    response = requests.post(url, headers=get_headers(), json=feature_data)
    return response.json()

def add_child_feature(parent, child_data):
    """Adds a child feature to a specific parent feature."""
    url = f"{BASE_URL}/feature-command/{parent}/add-child"
    response = requests.post(url, headers=get_headers(), json=child_data)
    return response.json()

def adopt_child_feature(parent, child):
    """Adopts a child feature into a specific parent feature."""
    url = f"{BASE_URL}/feature-command/{parent}/adopt/{child}"
    response = requests.post(url, headers=get_headers())
    return response.json()

def add_actor(project, actor_data):
    """Adds an actor to a specific project."""
    url = f"{BASE_URL}/actor-command/{project}/add"
    response = requests.post(url, headers=get_headers(), json=actor_data)
    return response.json()

def add_story_to_actor(project, name, story_data):
    """Adds a story to a specific actor in a project."""
    url = f"{BASE_URL}/actor-command/{project}/{name}/add-story"
    response = requests.post(url, headers=get_headers(), json=story_data)
    return response.json()

def normalize_tasks():
    """Normalizes tasks across the system."""
    url = f"{BASE_URL}/normalize-tasks"
    response = requests.get(url, headers=get_headers())
    return response.json()

def get_diagram_definition(name):
    """Retrieves the definition of a specific diagram identified by its name."""
    url = f"{BASE_URL}/diagram/plant-definition/{name}"
    response = requests.get(url, headers=get_headers())
    return response.json()

def update_diagram_definition(name, definition_data):
    """Updates the definition of a specific diagram identified by its name."""
    url = f"{BASE_URL}/diagram/update/{name}"
    response = requests.patch(url, headers=get_headers(), json=definition_data)
    return response.json()

