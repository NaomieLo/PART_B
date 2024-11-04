import requests

API_URL = "http://localhost:4567"


def capture_initial_state(context):
    context.initial_projects = []
    context.initial_categories = []

    try:
        # Capture initial state of projects
        projects_response = requests.get(f"{API_URL}/projects")
        projects = projects_response.json().get("projects", [])
        for project in projects:
            # Get categories for each project
            categories_response = requests.get(f"{API_URL}/projects/{project['id']}/categories")
            categories = categories_response.json().get("categories", [])

            context.initial_projects.append(
                {
                    "id": project["id"],
                    "title": project["title"],
                    "description": project.get("description", ""),
                    "active": project.get("active", "false"),
                    "completed": project.get("completed", "false"),
                    "categories": categories,
                }
            )

        # Capture initial state of standalone categories
        categories_response = requests.get(f"{API_URL}/categories")
        categories = categories_response.json().get("categories", [])
        for category in categories:
            context.initial_categories.append(
                {
                    "id": category["id"],
                    "title": category["title"],
                    "description": category.get("description", ""),
                }
            )

    except requests.ConnectionError:
        print(f"Could not connect to the API at {API_URL}")
        exit(1)
def restore_initial_state(context):
    # Fetch the current state of projects and categories
    projects_response = requests.get(f"{API_URL}/projects")
    projects = projects_response.json().get("projects", []) if projects_response.status_code == 200 else []

    categories_response = requests.get(f"{API_URL}/categories")
    categories = categories_response.json().get("categories", []) if categories_response.status_code == 200 else []

    # Delete any new projects that were added during the test
    for project in projects:
        if project["title"] not in [initial_project["title"] for initial_project in context.initial_projects]:
            delete_response = requests.delete(f"{API_URL}/projects/{project['id']}")
            assert delete_response.status_code in [200, 204], f"Failed to delete project with title '{project['title']}'"

    # Restore initial projects and their categories
    for initial_project in context.initial_projects:
        existing_project = next((project for project in projects if project["title"] == initial_project["title"]), None)

        if existing_project:
            # Update project if attributes changed
            if (
                existing_project.get("description", "") != initial_project["description"]
                or existing_project.get("active", "false") != initial_project["active"]
                or existing_project.get("completed", "false") != initial_project["completed"]
            ):
                update_data = {
                    "title": initial_project["title"],
                    "description": initial_project["description"],
                    "active": bool(initial_project["active"] == "true"),  # Convert to boolean
                    "completed": bool(initial_project["completed"] == "true"),  # Convert to boolean
                }
                print(f"Updating project '{initial_project['title']}' with data: {update_data}")
                update_response = requests.put(f"{API_URL}/projects/{existing_project['id']}", json=update_data)
                assert update_response.status_code in [200, 204], f"Failed to update project '{initial_project['title']}'"

            # Restore associated categories
            current_categories_response = requests.get(f"{API_URL}/projects/{existing_project['id']}/categories")
            current_categories = current_categories_response.json().get("categories", [])

            for category in current_categories:
                if category not in initial_project["categories"]:
                    delete_response = requests.delete(f"{API_URL}/projects/{existing_project['id']}/categories/{category['id']}")
                    assert delete_response.status_code in [200, 204], f"Failed to delete category '{category['title']}'"

            for category in initial_project["categories"]:
                if category not in current_categories:
                    print(f"Adding category '{category['title']}' to project '{initial_project['title']}'")
                    create_response = requests.post(f"{API_URL}/projects/{existing_project['id']}/categories", json=category)
                    assert create_response.status_code == 201, f"Failed to add category '{category['title']}' to project '{initial_project['title']}'"

        else:
            # Re-create missing project
            create_data = {
                "title": initial_project["title"],
                "description": initial_project["description"],
                "active": bool(initial_project["active"] == "true"),  # Convert to boolean
                "completed": bool(initial_project["completed"] == "true"),  # Convert to boolean
            }
            print(f"Creating project '{initial_project['title']}' with data: {create_data}")
            create_response = requests.post(f"{API_URL}/projects", json=create_data)
            assert create_response.status_code == 201, f"Failed to recreate project '{initial_project['title']}'"
            new_project_id = create_response.json()["id"]

            for category in initial_project["categories"]:
                print(f"Adding category '{category['title']}' to recreated project '{initial_project['title']}'")
                create_response = requests.post(f"{API_URL}/projects/{new_project_id}/categories", json=category)
                assert create_response.status_code == 201, f"Failed to add category '{category['title']}' to project '{initial_project['title']}'"

    # Delete any new categories that were added during the test
    for category in categories:
        if category["title"] not in [initial_category["title"] for initial_category in context.initial_categories]:
            delete_response = requests.delete(f"{API_URL}/categories/{category['id']}")
            assert delete_response.status_code in [200, 204], f"Failed to delete category with title '{category['title']}'"

    # Restore standalone categories
    for initial_category in context.initial_categories:
        existing_category = next((category for category in categories if category["title"] == initial_category["title"]), None)

        if existing_category:
            if existing_category.get("description", "") != initial_category["description"]:
                update_data = {
                    "title": initial_category["title"],
                    "description": initial_category["description"],
                }
                print(f"Updating standalone category '{initial_category['title']}' with data: {update_data}")
                update_response = requests.put(f"{API_URL}/categories/{existing_category['id']}", json=update_data)
                assert update_response.status_code in [200, 204], f"Failed to update category '{initial_category['title']}'"
        else:
            # Re-create missing standalone category
            data = {
                "title": initial_category["title"],
                "description": initial_category["description"],
            }
            print(f"Creating standalone category '{initial_category['title']}' with data: {data}")
            create_response = requests.post(f"{API_URL}/categories", json=data)
            assert create_response.status_code == 201, f"Failed to recreate category '{initial_category['title']}'"


def before_all(context):
    print("Setting up initial state...")
    capture_initial_state(context)


def after_scenario(context, scenario):
    print(f"Restoring initial state after scenario: {scenario.name}")
    restore_initial_state(context)
