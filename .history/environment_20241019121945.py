import requests

API_URL = "http://localhost:4567"


def capture_initial_state(context):
    context.initial_todos = []
    context.initial_categories = []

    try:
        # TODOS
        todos_response = requests.get(f"{API_URL}/todos")
        todos = todos_response.json().get("todos", [])
        for todo in todos:
            context.initial_todos.append(
                {
                    "title": todo["title"],
                    "description": todo.get("description", ""),
                    "doneStatus": todo.get("doneStatus", "false"),
                }
            )

        # CATEGORIES
        categories_response = requests.get(f"{API_URL}/categories")
        categories = categories_response.json().get("categories", [])
        for category in categories:
            context.initial_categories.append(
                {
                    "title": category["title"],
                    "description": category.get("description", ""),
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

    # TODOS
    current_todo_titles = {todo["title"] for todo in todos}

    # delete anything addded
    for todo in todos:
        if todo["title"] not in [
            initial_todo["title"] for initial_todo in context.initial_todos
        ]:
            delete_response = requests.delete(f"{API_URL}/todos/{todo['id']}")
            assert (
                delete_response.status_code == 200
            ), f"Failed to delete todo with title {todo['title']}"

    # re post or revert init states
    for initial_todo in context.initial_todos:
        existing_todo = next(
            (todo for todo in todos if todo["title"] == initial_todo["title"]), None
        )

        if existing_todo:

            if (
                existing_todo["description"] != initial_todo["description"]
                or str(existing_todo.get("doneStatus", "false")).lower()
                != str(initial_todo["doneStatus"]).lower()
            ):
                update_data = {
                    "title": initial_todo["title"],
                    "description": initial_todo["description"],
                    # ensure bool
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
        else:

            data = {
                "title": initial_todo["title"],
                "description": initial_todo["description"],
                # ensure bool
                "doneStatus": (
                    True if initial_todo["doneStatus"].lower() == "true" else False
                ),
            }
            create_response = requests.post(f"{API_URL}/todos", json=data)

    # CATEGORIES
    current_task_titles = {category["title"] for category in categories}

    # delete anything added
    for category in categories:
        if category["title"] not in [
            initial_task["title"] for initial_task in context.initial_categories
        ]:
            delete_response = requests.delete(f"{API_URL}/categories/{category['id']}")
            assert (
                delete_response.status_code == 200
            ), f"Failed to delete category with title {category['title']}"

    # re post or revert init states
    for initial_task in context.initial_categories:
        existing_category = next(
            (
                category
                for category in categories
                if category["title"] == initial_task["title"]
            ),
            None,
        )

        if existing_category:
            if existing_category.get("description", "") != initial_task["description"]:
                update_data = {
                    "title": initial_task["title"],
                    "description": initial_task["description"],
                }
                update_response = requests.put(
                    f"{API_URL}/categories/{existing_category['id']}", json=update_data
                )
                assert (
                    update_response.status_code == 200
                ), f"Failed to update category with title {initial_task['title']}"
                print(f"Updated category with title {initial_task['title']}")
        else:
            data = {
                "title": initial_task["title"],
                "description": initial_task["description"],
            }
            create_response = requests.post(f"{API_URL}/categories", json=data)


def before_all(context):
    capture_initial_state(context)


def after_scenario(context, scenario):
    restore_initial_state(context)
