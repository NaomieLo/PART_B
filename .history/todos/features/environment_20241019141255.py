import requests

API_URL = "http://localhost:4567"


def capture_initial_state(context):
    context.initial_todos = []
    context.initial_categories = []
    context.initial_projects = {}

    try:
        # todos 
        todos_response = requests.get(f"{API_URL}/todos")
        todos = todos_response.json().get("todos", [])
        for todo in todos:
            # tasks
            tasksof_response = requests.get(f"{API_URL}/todos/{todo['id']}/tasksof")
            tasksof = tasksof_response.json().get("projects", [])

            # categeories 
            categories_response = requests.get(f"{API_URL}/todos/{todo['id']}/categories")
            categories = categories_response.json().get("categories", [])

            context.initial_todos.append(
                {
                    "id": todo["id"],
                    "title": todo["title"],
                    "description": todo.get("description", ""),
                    "doneStatus": todo.get("doneStatus", "false"),
                    "tasksof": tasksof, 
                    "categories": categories, 
                }
            )

        # category  
        categories_response = requests.get(f"{API_URL}/categories")
        categories = categories_response.json().get("categories", [])
        for category in categories:
            context.initial_categories.append(
                {
                    "title": category["title"],
                    "description": category.get("description", ""),
                }
            )

        # projects  
        projects_response = requests.get(f"{API_URL}/projects")
        projects = projects_response.json().get("projects", [])
        for project in projects:
            context.initial_projects[project["id"]] = {
                "id": project["id"],
                "title": project["title"],
                "description": project.get("description", ""),
                "active": project.get("active", ""),
                "completed": project.get("completed", ""),
            }

    # FAIL if not connected to API 
    except requests.ConnectionError:

        print(f"Could not connect to the API at {API_URL}")
        exit(1)

def restore_initial_state(context):

    # fetch the data for todos 
    todos_response = requests.get(f"{API_URL}/todos")
    todos = todos_response.json().get("todos", []) if todos_response.status_code == 200 else []

    # fetch the data for categories 
    categories_response = requests.get(f"{API_URL}/categories")
    categories = categories_response.json().get("categories", []) if categories_response.status_code == 200 else []

    # fetch the data for project 
    projects_response = requests.get(f"{API_URL}/projects")
    projects = projects_response.json().get("projects", []) if projects_response.status_code == 200 else []


    # delete any new instances of todos 
    for todo in todos:
        if todo["title"] not in [initial_todo["title"] for initial_todo in context.initial_todos]:
            delete_response = requests.delete(f"{API_URL}/todos/{todo['id']}")
            assert delete_response.status_code == 200, f"Failed to delete todo with title {todo['title']}"

    # re post or fix existing for todos 
    for initial_todo in context.initial_todos:
        existing_todo = next((todo for todo in todos if todo["title"] == initial_todo["title"]), None)

        # fix if any updates were made
        if existing_todo:
            if (
                existing_todo["description"] != initial_todo["description"]
                or str(existing_todo.get("doneStatus", "false")).lower()
                != str(initial_todo["doneStatus"]).lower()
            ):
                update_data = {
                    "title": initial_todo["title"],
                    "description": initial_todo["description"],
                    "doneStatus": True if initial_todo["doneStatus"].lower() == "true" else False,
                }
                update_response = requests.put(f"{API_URL}/todos/{existing_todo['id']}", json=update_data)
                assert update_response.status_code == 200, f"Failed to update todo with title {initial_todo['title']}"

            # re add or fix tasksofs
            current_projects_response = requests.get(f"{API_URL}/todos/{existing_todo['id']}/tasksof")
            current_projects = current_projects_response.json().get("projects", [])

            for project in current_projects:
                if project not in initial_todo["tasksof"]:
                    delete_response = requests.delete(f"{API_URL}/todos/{existing_todo['id']}/tasksof/{project['id']}")
                    assert delete_response.status_code == 200, f"Failed to delete project '{project['title']}'"

            for project in initial_todo["tasksof"]:
                if project not in current_projects:
                    create_response = requests.post(f"{API_URL}/todos/{existing_todo['id']}/tasksof", json=project)
                    assert create_response.status_code == 201, f"Failed to add project '{project['title']}'"

             # re add or fix categories 
            current_categories_response = requests.get(f"{API_URL}/todos/{existing_todo['id']}/categories")
            current_categories = current_categories_response.json().get("categories", [])

            for category in current_categories:
                if category not in initial_todo["categories"]:
                    delete_response = requests.delete(f"{API_URL}/todos/{existing_todo['id']}/categories/{category['id']}")
                    assert delete_response.status_code == 200, f"Failed to delete category '{category['title']}'"

            for category in initial_todo["categories"]:
                if category not in current_categories:
                    create_response = requests.post(f"{API_URL}/todos/{existing_todo['id']}/categories", json=category)
                    assert create_response.status_code == 201, f"Failed to add category '{category['title']}'"

        # re post if no longer exists
        else:
            data = {
                "title": initial_todo["title"],
                "description": initial_todo["description"],
                "doneStatus": True if initial_todo["doneStatus"].lower() == "true" else False,
            }
            create_response = requests.post(f"{API_URL}/todos", json=data)
            assert create_response.status_code == 201, f"Failed to create todo '{initial_todo['title']}'"

            new_todo_id = create_response.json()["id"]

            for project in initial_todo["tasksof"]:
                create_response = requests.post(f"{API_URL}/todos/{new_todo_id}/tasksof", json=project)
                assert create_response.status_code == 201, f"Failed to add project '{project['title']}'"

            for category in initial_todo["categories"]:
                create_response = requests.post(f"{API_URL}/todos/{new_todo_id}/categories", json=category)
                assert create_response.status_code == 201, f"Failed to add category '{category['title']}'"

    # delete any new instances of categories 
    for category in categories:
        if category["title"] not in [initial_category["title"] for initial_category in context.initial_categories]:
            delete_response = requests.delete(f"{API_URL}/categories/{category['id']}")
            assert delete_response.status_code == 200, f"Failed to delete category with title {category['title']}"

     # re post or fix existing for todos 
    for initial_category in context.initial_categories:
        existing_category = next(
            (category for category in categories if category["title"] == initial_category["title"]),
            None,
        )


        # update if still there
        if existing_category:
            if existing_category.get("description", "") != initial_category["description"]:
                update_data = {
                    "title": initial_category["title"],
                    "description": initial_category["description"],
                }
                update_response = requests.put(f"{API_URL}/categories/{existing_category['id']}", json=update_data)
                assert update_response.status_code == 200, f"Failed to update category with title {initial_category['title']}"
        
        #re post if got deleted 
        else:
            data = {
                "title": initial_category["title"],
                "description": initial_category["description"],
            }
            create_response = requests.post(f"{API_URL}/categories", json=data)
    
    

    # delete any new instances of projects  
    for category in categories:
        if category["title"] not in [initial_category["title"] for initial_category in context.initial_categories]:
            delete_response = requests.delete(f"{API_URL}/categories/{category['id']}")
            assert delete_response.status_code == 200, f"Failed to delete category with title {category['title']}"

     # re post or fix existing for todos 
    for initial_category in context.initial_categories:
        existing_category = next(
            (category for category in categories if category["title"] == initial_category["title"]),
            None,
        )


        # update if still there
        if existing_category:
            if existing_category.get("description", "") != initial_category["description"]:
                update_data = {
                    "title": initial_category["title"],
                    "description": initial_category["description"],
                }
                update_response = requests.put(f"{API_URL}/categories/{existing_category['id']}", json=update_data)
                assert update_response.status_code == 200, f"Failed to update category with title {initial_category['title']}"
        
        #re post if got deleted 
        else:
            data = {
                "title": initial_category["title"],
                "description": initial_category["description"],
            }
            create_response = requests.post(f"{API_URL}/categories", json=data)
    
    

def before_all(context):
    capture_initial_state(context)


def after_scenario(context, scenario):
    restore_initial_state(context)
