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
        categories_response = requests.get(f"{API_URL}/project")
        categories = categories_response.json().get("project", [])
        for category in categories:
            context.initial_categories.append(
                {
                    "id": project["id"],
                    "title": todo["title"],
                    "description": todo.get("description", ""),
                    "active": todo.get("doneStatus", "false"),
                    "completed": tasksof, 
                }
            )

    except requests.ConnectionError:
        # Stop program if API is not running
        print(f"Could not connect to the API at {API_URL}")
        exit(1)


def restore_initial_state(context):
    todos_response = requests.get(f"{API_URL}/todos")
    todos = (
        todos_response.json().get("todos", [])
        if todos_response.status_code == 200
        else []
    )

    categories_response = requests.get(f"{API_URL}/categories")
    categories = (
        categories_response.json().get("categories", [])
        if categories_response.status_code == 200
        else []
    )

    # Restore Todos and their associated projects and categories
    for todo in todos:
        if todo["title"] not in [
            initial_todo["title"] for initial_todo in context.initial_todos
        ]:
            # Delete any todo that wasn't in the initial state
            delete_response = requests.delete(f"{API_URL}/todos/{todo['id']}")
            assert (
                delete_response.status_code == 200
            ), f"Failed to delete todo with title {todo['title']}"

    for initial_todo in context.initial_todos:
        existing_todo = next(
            (todo for todo in todos if todo["title"] == initial_todo["title"]), None
        )

        if existing_todo:
            # Update if todo description or doneStatus changed
            if (
                existing_todo["description"] != initial_todo["description"]
                or str(existing_todo.get("doneStatus", "false")).lower()
                != str(initial_todo["doneStatus"]).lower()
            ):
                update_data = {
                    "title": initial_todo["title"],
                    "description": initial_todo["description"],
                    "doneStatus": (
                        True if initial_todo["doneStatus"].lower() == "true" else False
                    ),
                }
                update_response = requests.put(
                    f"{API_URL}/todos/{existing_todo['id']}", json=update_data
                )
                assert (
                    update_response.status_code == 200
                ), f"Failed to update todo with title {initial_todo['title']}"

            # Restore projects (tasksof)
            current_projects_response = requests.get(
                f"{API_URL}/todos/{existing_todo['id']}/tasksof"
            )
            current_projects = current_projects_response.json().get("projects", [])

            for project in current_projects:
                if project not in initial_todo["tasksof"]:
                    delete_response = requests.delete(
                        f"{API_URL}/todos/{existing_todo['id']}/tasksof/{project['id']}"
                    )
                    assert (
                        delete_response.status_code == 200
                    ), f"Failed to delete project '{project['title']}'"

            # Re-add or update projects (tasksof)
            for project in initial_todo["tasksof"]:
                if project not in current_projects:
                    create_response = requests.post(
                        f"{API_URL}/todos/{existing_todo['id']}/tasksof", json=project
                    )
                    assert (
                        create_response.status_code == 201
                    ), f"Failed to add project '{project['title']}'"

            # Restore categories
            current_categories_response = requests.get(
                f"{API_URL}/todos/{existing_todo['id']}/categories"
            )
            current_categories = current_categories_response.json().get("categories", [])

            for category in current_categories:
                if category not in initial_todo["categories"]:
                    delete_response = requests.delete(
                        f"{API_URL}/todos/{existing_todo['id']}/categories/{category['id']}"
                    )
                    assert (
                        delete_response.status_code == 200
                    ), f"Failed to delete category '{category['title']}'"

            # Re-add or update categories
            for category in initial_todo["categories"]:
                if category not in current_categories:
                    create_response = requests.post(
                        f"{API_URL}/todos/{existing_todo['id']}/categories", json=category
                    )
                    assert (
                        create_response.status_code == 201
                    ), f"Failed to add category '{category['title']}'"

        else:
            # Recreate missing todo and its associated projects and categories
            data = {
                "title": initial_todo["title"],
                "description": initial_todo["description"],
                "doneStatus": (
                    True if initial_todo["doneStatus"].lower() == "true" else False
                ),
            }
            create_response = requests.post(f"{API_URL}/todos", json=data)
            assert create_response.status_code == 201, f"Failed to create todo '{initial_todo['title']}'"

            new_todo_id = create_response.json()["id"]

            # Re-add projects (tasksof) for the recreated todo
            for project in initial_todo["tasksof"]:
                create_response = requests.post(
                    f"{API_URL}/todos/{new_todo_id}/tasksof", json=project
                )
                assert (
                    create_response.status_code == 201
                ), f"Failed to add project '{project['title']}'"

            # Re-add categories for the recreated todo
            for category in initial_todo["categories"]:
                create_response = requests.post(
                    f"{API_URL}/todos/{new_todo_id}/categories", json=category
                )
                assert (
                    create_response.status_code == 201
                ), f"Failed to add category '{category['title']}'"

    # Restore Global Categories
    for category in categories:
        if category["title"] not in [
            initial_category["title"] for initial_category in context.initial_categories
        ]:
            delete_response = requests.delete(f"{API_URL}/categories/{category['id']}")
            assert (
                delete_response.status_code == 200
            ), f"Failed to delete category with title {category['title']}"

    for initial_category in context.initial_categories:
        existing_category = next(
            (
                category
                for category in categories
                if category["title"] == initial_category["title"]
            ),
            None,
        )

        if existing_category:
            if existing_category.get("description", "") != initial_category["description"]:
                update_data = {
                    "title": initial_category["title"],
                    "description": initial_category["description"],
                }
                update_response = requests.put(
                    f"{API_URL}/categories/{existing_category['id']}", json=update_data
                )
                assert (
                    update_response.status_code == 200
                ), f"Failed to update category with title {initial_category['title']}"
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
