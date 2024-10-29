import requests
from behave import given, when, then

API_URL = "http://localhost:4567"

# Helper function to get the project ID given a title
def get_project_id(title):
    response = requests.get(f"{API_URL}/projects")
    assert response.status_code == 200, "Failed to retrieve projects."
    projects = response.json().get("projects", [])
    for project in projects:
        if project["title"] == title:
            return project["id"]
    return None

# Helper function to get all projects
def get_all_projects():
    response = requests.get(f"{API_URL}/projects")
    assert response.status_code == 200, "Failed to retrieve projects."
    return response.json().get("projects", [])

# Helper function to get categories of a project
def get_categories_of_project(project_id):
    response = requests.get(f"{API_URL}/projects/{project_id}/categories")
    assert response.status_code == 200, "Failed to retrieve categories."
    return response.json().get("categories", [])

@given("there are multiple projects in the database")
def step_impl(context):
    # Create multiple projects if they don’t exist already
    project_titles = ["Grocery Shopping", "Complete Homework", "Pay Bills"]
    for title in project_titles:
        if not any(project["title"] == title for project in get_all_projects()):
            data = {"title": title, "description": f"{title} description"}
            response = requests.post(f"{API_URL}/projects", json=data)
            assert response.status_code == 201, f"Failed to create project '{title}'"

@given("the API is responsive")
def step_impl(context):
    try:
        response = requests.get(API_URL)
        assert response.status_code == 200, "API is not active"
        context.api_is_running = True
    except requests.ConnectionError:
        context.api_is_running = False
        assert False, "Could not connect to the API"

@given("there is an existing project with title '{project_title}' in the database")
def step_impl(context, project_title):
    project_id = get_project_id(project_title)
    if project_id is None:
        # Project doesn't exist, so create it
        data = {"title": project_title}
        response = requests.post(f"{API_URL}/projects", json=data)
        assert response.status_code == 201, f"Failed to create project '{project_title}'"
        context.project_id = response.json()["id"]
    else:
        # Project exists, store its ID in context
        context.project_id = project_id

@given("there is a second project with title '{project_title}' in the database")
def step_impl(context, project_title):
    # Create a second instance of the project with the same title
    data = {"title": project_title}
    response = requests.post(f"{API_URL}/projects", json=data)
    assert response.status_code == 201, f"Failed to create second project '{project_title}'"
    context.second_project_id = response.json()["id"]

@given("the database is empty")
def step_impl(context):
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])

    for project in projects:
        requests.delete(f"{API_URL}/projects/{project['id']}")
    
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])
    assert len(projects) == 0, "Database is not empty after deletion."

@given("the project with title '{project_title}' already has categories '{category1}' and '{category2}'")
def step_impl(context, project_title, category1, category2):
    project_id = get_project_id(project_title)
    assert project_id is not None, f"Project with title '{project_title}' not found."

    def ensure_category_exists(category_title):
        response = requests.get(f"{API_URL}/categories")
        categories = response.json().get("categories", [])
        category_id = next((cat["id"] for cat in categories if cat["title"] == category_title), None)
        if category_id is None:
            data = {"title": category_title}
            response = requests.post(f"{API_URL}/categories", json=data)
            assert response.status_code == 201, f"Failed to create category '{category_title}'"
            category_id = response.json()["id"]
        return category_id

    category1_id = ensure_category_exists(category1)
    category2_id = ensure_category_exists(category2)

    response = requests.get(f"{API_URL}/projects/{project_id}/categories")
    existing_categories = response.json().get("categories", [])
    existing_category_titles = [cat["title"] for cat in existing_categories]

    if category1 not in existing_category_titles:
        requests.post(f"{API_URL}/projects/{project_id}/categories", json={"id": category1_id})

    if category2 not in existing_category_titles:
        requests.post(f"{API_URL}/projects/{project_id}/categories", json={"id": category2_id})
   
@given("the project with title '{project_title}' has no categories")
def step_impl(context, project_title):
    project_id = get_project_id(project_title)
    assert project_id is not None, f"Project '{project_title}' not found."

    # Remove any existing categories for the project
    categories = get_categories_of_project(project_id)
    for category in categories:
        response = requests.delete(f"{API_URL}/projects/{project_id}/categories/{category['id']}")
        assert response.status_code == 200, f"Failed to remove category '{category['id']}' from project '{project_id}'"

@given("there is no project with ID {project_id} in the database")
def step_impl(context, project_id):
    # Ensure the project with the specified ID does not exist
    response = requests.get(f"{API_URL}/projects/{project_id}")
    if response.status_code == 200:
        requests.delete(f"{API_URL}/projects/{project_id}")
    context.non_existent_project_id = project_id

@when("the user deletes the project with title '{project_title}'")
def step_impl(context, project_title):
    project_id = get_project_id(project_title)
    assert project_id is not None, f"Project '{project_title}' not found for deletion."
    context.response = requests.delete(f"{API_URL}/projects/{project_id}")

@when("the user attempts to delete a project with id {project_id}")
def step_impl(context, project_id):
    context.response = requests.delete(f"{API_URL}/projects/{project_id}")

@when("the user retrieves all projects")
def step_impl(context):
    context.response = requests.get(f"{API_URL}/projects")

@when("the user attempts to retrieve a project with id {project_id}")
def step_impl(context, project_id):
    context.response = requests.get(f"{API_URL}/projects/{project_id}")

@when("the user creates a project with title '{title}'")
def step_impl(context, title):
    data = {"title": title}
    context.response = requests.post(f"{API_URL}/projects", json=data)

@when("the user attempts to create a project with title '{title}'")
def step_impl(context, title):
    data = {"title": title}
    context.response = requests.post(f"{API_URL}/projects", json=data)

@when("the user posts the category '{category_title}' for the project with title '{project_title}'")
def step_impl(context, category_title, project_title):
    project_id = get_project_id(project_title)
    assert project_id is not None, f"Project with title '{project_title}' not found."

    data = {"title": category_title}
    context.response = requests.post(f"{API_URL}/projects/{project_id}/categories", json=data)

@when("the user attempts to post the category '{category_title}' for a non-existent project")
def step_impl(context, category_title):
    non_existent_project_id = 123456789  # Arbitrary ID for non-existent project
    data = {"title": category_title}
    context.response = requests.post(f"{API_URL}/projects/{non_existent_project_id}/categories", json=data)

@when("the user updates the project with title '{old_title}' to have title '{new_title}' and description '{new_description}'")
def step_impl(context, old_title, new_title, new_description):
    project_id = get_project_id(old_title)
    assert project_id is not None, f"Project '{old_title}' not found for update."

    data = {"title": new_title, "description": new_description}
    context.response = requests.put(f"{API_URL}/projects/{project_id}", json=data)

@when("the user updates the project with title '{old_title}' to have title '{new_title}'")
def step_impl(context, old_title, new_title):
    project_id = get_project_id(old_title)
    assert project_id is not None, f"Project '{old_title}' not found for update."

    data = {"title": new_title}
    context.response = requests.put(f"{API_URL}/projects/{project_id}", json=data)

@when("the user attempts to update a project with id {project_id}")
def step_impl(context, project_id):
    data = {"title": "Non-existent Project", "description": "This should fail"}
    context.response = requests.put(f"{API_URL}/projects/{project_id}", json=data)

@when("the user retrieves the categories for the project with title '{project_title}'")
def step_impl(context, project_title):
    project_id = get_project_id(project_title)
    assert project_id is not None, f"Project '{project_title}' not found."
    context.response = requests.get(f"{API_URL}/projects/{project_id}/categories")

@when("the user attempts to retrieve categories for the project with ID {project_id}")
def step_impl(context, project_id):
    context.response = requests.get(f"{API_URL}/projects/{project_id}/categories")

@then("the status code {status_code:d} will be received")
def step_impl(context, status_code):
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"

@then("the project with title '{project_title}' should no longer exist in the database")
def step_impl(context, project_title):
    project_id = get_project_id(project_title)
    assert project_id is None, f"Project '{project_title}' still exists in the database."

@then("only one project with title '{project_title}' should exist in the database")
def step_impl(context, project_title):
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])
    projects_with_title = [project for project in projects if project["title"] == project_title]
    assert len(projects_with_title) == 1, f"Expected only one project with title '{project_title}', but found {len(projects_with_title)}."

@then("an error message '{error_message}' will be displayed")
def step_impl(context, error_message):
    error_message_received = context.response.json().get("errorMessage", "")
    assert error_message in error_message_received, f"Expected error message '{error_message}', but got '{error_message_received}'"
    
@then("the error message will be empty")
def step_impl(context):
    error_message_received = context.response.json().get("errorMessage", "")
    assert error_message_received == "", f"Expected an empty error message, but got '{error_message_received}'"

@then("the project with new title '{new_title}' has new description '{new_description}'")
def step_impl(context, new_title, new_description):
    project_id = get_project_id(new_title)
    assert project_id is not None, f"Project '{new_title}' not found."

    response = requests.get(f"{API_URL}/projects/{project_id}")
    assert response.status_code == 200, f"Failed to retrieve project with id '{project_id}'. Response: {response.text}"

    project_data = response.json().get("projects", [])
    assert len(project_data) > 0, f"No project data found in response: {response.json()}"

    project = project_data[0] 
    print("Project response:", project)  

    assert "title" in project, f"Expected 'title' in response, but got: {project}"
    assert "description" in project, f"Expected 'description' in response, but got: {project}"

    assert project["title"] == new_title, f"Expected title '{new_title}', but got '{project.get('title')}'"
    assert project["description"] == new_description, f"Expected description '{new_description}', but got '{project.get('description')}'"

@then("the project with title '{project_title}' should exist in the database")
def step_impl(context, project_title):
    response = requests.get(f"{API_URL}/projects")
    projects = response.json().get("projects", [])
    assert any(project["title"] == project_title for project in projects), f"Project '{project_title}' not found in the database."

@then("the response contains a list of projects")
def step_impl(context):
    projects = context.response.json().get("projects", [])
    assert isinstance(projects, list), "Expected 'projects' to be a list."
    assert len(projects) > 0, "Expected a non-empty list of projects but got empty."

@then('the project with title "{project_title}" is included in the list')
def step_impl(context, project_title):
    projects = get_all_projects()
    assert any(project["title"] == project_title for project in projects), f"Project '{project_title}' not found in the list of projects."

@then("the response contains an empty list for 'projects'")
def step_impl(context):
    projects = context.response.json().get("projects", [])
    assert projects == [], "Expected 'projects' to be an empty list, but got non-empty data."

@then("the response contains categories '{category1}, {category2}, {category3}' for the project with the title '{project_title}'")
def step_impl(context, category1, category2, category3, project_title):
    project_id = get_project_id(project_title)
    assert project_id is not None, f"Project '{project_title}' not found."

    response = requests.get(f"{API_URL}/projects/{project_id}/categories")
    categories = response.json().get("categories", [])
    category_titles = [category["title"] for category in categories]

    for expected_category in [category1, category2, category3]:
        assert expected_category in category_titles, f"Category '{expected_category}' not found for project '{project_title}'."

@then("the response contains categories '{category_titles}' for the project with the title '{project_title}'")
def step_impl(context, category_titles, project_title):
    project_id = get_project_id(project_title)
    assert project_id is not None, f"Project '{project_title}' not found."

    # Retrieve categories linked to the project
    response = requests.get(f"{API_URL}/projects/{project_id}/categories")
    categories = response.json().get("categories", [])
    category_titles_list = [title.strip() for title in category_titles.split(",")]

    # Check if each expected category is in the retrieved categories
    existing_category_titles = [category["title"] for category in categories]
    for expected_category in category_titles_list:
        assert expected_category in existing_category_titles, f"Category '{expected_category}' not found for project '{project_title}'."

@then("the response contains an empty list for 'categories'")
def step_impl(context):
    categories = context.response.json().get("categories", [])
    assert categories == [], f"Expected an empty list of categories, but got {categories}"
