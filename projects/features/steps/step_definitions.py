import requests
from behave import given, when, then

API_URL = "http://localhost:4567"

@given("the API is responsive")
def step_impl(context):
    response = requests.get(API_URL)
    assert response.status_code == 200, "API is not active"

@given("there are multiple projects in the database")
def step_impl(context):
    # Assuming "Project Alpha" is a sample project in the database
    data = {"title": "Project Alpha"}
    response = requests.post(f"{API_URL}/projects", json=data)
    assert response.status_code == 201, "Failed to create 'Project Alpha'"

@given("the database is empty")
def step_impl(context):
    # Clear out any existing projects
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])
    for project in projects:
        requests.delete(f"{API_URL}/projects/{project['id']}")

@when("the user retrieves all projects")
def step_impl(context):
    context.response = requests.get(f"{API_URL}/projects")

@when("the user attempts to retrieve a project with id {project_id}")
def step_impl(context, project_id):
    context.response = requests.get(f"{API_URL}/projects/{project_id}")

@then("the status code {status_code:d} will be received")
def step_impl(context, status_code):
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"

@then("the response contains a list of projects")
def step_impl(context):
    projects = context.response.json().get("projects", [])
    assert len(projects) > 0, "Expected list of projects but got empty"

@then('the response contains an empty list for "{key}"')
def step_impl(context, key):
    data_list = context.response.json().get(key, [])
    assert data_list == [], f"Expected empty list for '{key}', but got: {data_list}"

@then("the project with title {project_title} is included in the list")
def step_impl(context, project_title):
    projects = context.response.json().get("projects", [])
    assert any(project["title"] == project_title for project in projects), f"Project '{project_title}' not found"

@then('an error message "{message}" will be displayed')
def step_impl(context, message):
    error_message = context.response.json().get("error", "")
    assert message in error_message, f"Expected error message '{message}', but got '{error_message}'"

@given("there is an existing project with title {project_title}")
def step_impl(context, project_title):
    # Create a project with the given title if it doesn't already exist
    data = {"title": project_title}
    requests.post(f"{API_URL}/projects", json=data)

@when("the user creates a project with title {title} and description {description}")
def step_impl(context, title, description):
    data = {"title": title, "description": description}
    context.response = requests.post(f"{API_URL}/projects", json=data)

@when("the user attempts to create a project with title {title}")
def step_impl(context, title):
    data = {"title": title}
    context.response = requests.post(f"{API_URL}/projects", json=data)

@then("the response will contain a project with title {title}")
def step_impl(context, title):
    project = context.response.json()
    assert project["title"] == title, f"Expected project title '{title}', but got '{project.get('title')}'"

@when("the user deletes the project with title {title}")
def step_impl(context, title):
    # Retrieve project ID based on title
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])
    project_id = next((project["id"] for project in projects if project["title"] == title), None)
    assert project_id is not None, f"Project '{title}' not found for deletion"
    
    # Perform delete action
    context.response = requests.delete(f"{API_URL}/projects/{project_id}")

@then("the project with title {title} should no longer exist in the database")
def step_impl(context, title):
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])
    assert not any(project["title"] == title for project in projects), f"Project '{title}' was not deleted"
    
@given("there is an existing project with title {project_title}")
def step_impl(context, project_title):
    # Create a project with the given title if it doesn't already exist
    data = {"title": project_title}
    requests.post(f"{API_URL}/projects", json=data)

@when("the user updates the project with title {old_title} to have title {new_title} and description {new_description}")
def step_impl(context, old_title, new_title, new_description):
    # Retrieve the project ID based on the old title
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])
    project_id = next((project["id"] for project in projects if project["title"] == old_title), None)
    assert project_id is not None, f"Project '{old_title}' not found for update"

    # Perform update action
    data = {"title": new_title, "description": new_description}
    context.response = requests.put(f"{API_URL}/projects/{project_id}", json=data)

@when("the user updates the project with title {old_title} to have title {new_title}")
def step_impl(context, old_title, new_title):
    # Retrieve the project ID based on the old title
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])
    project_id = next((project["id"] for project in projects if project["title"] == old_title), None)
    assert project_id is not None, f"Project '{old_title}' not found for update"

    # Perform update action with only the new title
    data = {"title": new_title}
    context.response = requests.put(f"{API_URL}/projects/{project_id}", json=data)

@when("the user attempts to update a project with id {project_id}")
def step_impl(context, project_id):
    # Try to update a project that doesn’t exist
    data = {"title": "Non-existent Project", "description": "This should fail"}
    context.response = requests.put(f"{API_URL}/projects/{project_id}", json=data)

@then("the project with title {title} should exist in the database")
def step_impl(context, title):
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])
    assert any(project["title"] == title for project in projects), f"Project '{title}' not found"

@given("there is a category with title {category_title}")
def step_impl(context, category_title):
    # Create a category with the given title if it doesn't already exist
    data = {"title": category_title}
    response = requests.post(f"{API_URL}/categories", json=data)
    assert response.status_code == 201, f"Failed to create category '{category_title}'"

@when("the user links the category {category_title} to the project with title {project_title}")
def step_impl(context, category_title, project_title):
    # Retrieve project ID
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])
    project_id = next((project["id"] for project in projects if project["title"] == project_title), None)
    assert project_id is not None, f"Project '{project_title}' not found for linking category"

    # Retrieve category ID
    response = requests.get(f"{API_URL}/categories")
    categories = response.json().get("categories", [])
    category_id = next((category["id"] for category in categories if category["title"] == category_title), None)
    assert category_id is not None, f"Category '{category_title}' not found for linking"

    # Perform link action
    context.response = requests.post(f"{API_URL}/projects/{project_id}/categories", json={"id": category_id})

@when("the user attempts to link the category {category_title} to a project with id {project_id}")
def step_impl(context, category_title, project_id):
    # Retrieve category ID
    response = requests.get(f"{API_URL}/categories")
    categories = response.json().get("categories", [])
    category_id = next((category["id"] for category in categories if category["title"] == category_title), None)
    assert category_id is not None, f"Category '{category_title}' not found for linking"

    # Attempt to link the category to a non-existent project
    context.response = requests.post(f"{API_URL}/projects/{project_id}/categories", json={"id": category_id})

@then("the project with title {project_title} will contain the category {category_title}")
def step_impl(context, project_title, category_title):
    # Retrieve project ID
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])
    project_id = next((project["id"] for project in projects if project["title"] == project_title), None)
    assert project_id is not None, f"Project '{project_title}' not found for verification"

    # Check if the project contains the category
    response = requests.get(f"{API_URL}/projects/{project_id}/categories")
    categories = response.json().get("categories", [])
    assert any(category["title"] == category_title for category in categories), f"Category '{category_title}' not linked to project '{project_title}'"
