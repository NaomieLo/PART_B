import requests
from behave import given, when, then

API_URL = "http://localhost:4567"


# Helper function to get the todo id given a title
def get_todo_id(title):
    response = requests.get(f"{API_URL}/todos")
    assert response.status_code == 200, "Failed to retrieve todos."
    todos = response.json().get("todos", [])
    for todo in todos:
        if todo["title"] == title:
            return todo["id"]
    return None


# Helper function to post new category
def post_category_for_todo(context, todo_title, category_title):

    todo_id = get_todo_id(todo_title)
    assert todo_id is not None, f"Todo with title '{todo_title}' not found."

    data = {"title": category_title}
    context.response = requests.post(f"{API_URL}/todos/{todo_id}/categories", json=data)
    assert (
        context.response.status_code == 201
    ), f"Failed to post category '{category_title}' for todo '{todo_title}'"


@given("the API is responsive")
def step_impl(context):
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            context.api_is_running = True
        else:
            context.api_is_running = False
            assert False, "API is not active"
    except requests.ConnectionError:
        context.api_is_running = False
        assert False, "Could not connect to the API"


@given("the database contains several todos")
def step_impl(context):
    if not context.api_is_running:
        return

    for title in ["Grocery Shopping", "Complete Homework", "Pay Bills"]:
        data = {"title": title, "description": f"Description for {title}"}
        response = requests.post(f"{API_URL}/todos", json=data)
        assert response.status_code == 201, f"Failed to create todo '{title}'"


@given("the database is empty")
def step_impl(context):
    if not context.api_is_running:
        return

    response = requests.get(f"{API_URL}/todos")
    todos = response.json().get("todos", [])

    for todo in todos:
        todo_id = todo["id"]
        delete_response = requests.delete(f"{API_URL}/todos/{todo_id}")


@given("there is an existing todo with title '{todo_title}' in the database")
def step_impl(context, todo_title):
    if not context.api_is_running:
        return

    todo_id = get_todo_id(todo_title)

    # only want to post once, post the instance if dne
    if todo_id:
        context.todo_id = todo_id
    else:

        data = {"title": todo_title}
        response = requests.post(f"{API_URL}/todos", json=data)
        assert (
            response.status_code == 201
        ), "Failed to create todo with title '{todo_title}'"
        context.todo_id = response.json()["id"]


@given("there is a second todo with title '{todo_title}' in the database")
def step_impl(context, todo_title):
    if not context.api_is_running:
        return

    data = {"title": todo_title}
    response = requests.post(f"{API_URL}/todos", json=data)
    assert (
        response.status_code == 201
    ), "Failed to create todo with title '{todo_title}'"
    context.todo_id = response.json()["id"]


@given(
    "the todo with title '{todo_title}' already has categories '{TASK1}' and '{TASK2}'"
)
def step_impl(context, todo_title, TASK1, TASK2):
    if not context.api_is_running:
        return

    # use helper to post many categories
    post_category_for_todo(context, todo_title, TASK1)
    post_category_for_todo(context, todo_title, TASK2)


@when("the user retrieves all todos")
def step_impl(context):
    if not context.api_is_running:
        return
    context.response = requests.get(f"{API_URL}/todos")


@when("the user attempts to retrieve a todo with id 9999")
def step_impl(context):
    if not context.api_is_running:
        return
    context.response = requests.get(f"{API_URL}/todos/9999")


@when("the user deletes the todo with title '{todo_title}'")
def step_impl(context, todo_title):
    if not context.api_is_running:
        return

    todo_id = get_todo_id(todo_title)
    if todo_id:
        context.response = requests.delete(f"{API_URL}/todos/{todo_id}")
    else:
        assert False, f"Todo with title '{todo_title}' not found"


@when("the user attempts to delete a todo with id 9999")
def step_impl(context):
    if not context.api_is_running:
        return
    context.response = requests.delete(f"{API_URL}/todos/9999")


@when(
    "the user posts the category '{category_title}' for the todo with title '{todo_title}'"
)
def step_impl(context, category_title, todo_title):
    if not context.api_is_running:
        return

    post_category_for_todo(context, todo_title, category_title)


@when(
    "the user attempts to post the category '{category_title}' for a non-existent todo"
)
def step_impl(context, category_title):
    if not context.api_is_running:
        return

    data = {"title": category_title}
    context.response = requests.post(f"{API_URL}/todos/9999/categories", json=data)


@when("the user attempts to update a todo with a non-existent todo")
def step_impl(context):
    if not context.api_is_running:
        return

    data = {"title": "title"}
    context.response = requests.put(f"{API_URL}/todos/9999", json=data)


@when(
    "the todo with title '{todo_title}' is updated with title '{new_title}', doneStatus '{doneStatus}', and description '{new_description}'"
)
def step_impl(context, todo_title, new_title, doneStatus, new_description):
    if not context.api_is_running:
        return

    doneStatus_bool = doneStatus.lower() == "true"

    data = {
        "title": new_title,
        "description": new_description,
        "doneStatus": doneStatus_bool,
    }

    todo_id = get_todo_id(todo_title)
    assert todo_id is not None, f"Todo with title '{todo_title}' not found."

    context.response = requests.put(f"{API_URL}/todos/{todo_id}", json=data)

    assert (
        context.response.status_code == 200
    ), f"Failed to update todo with id '{todo_id}'. Response: {context.response.text}"


@when("the todo with title '{todo_title}' is updated with title '{new_title}'")
def step_impl(context, todo_title, new_title):
    if not context.api_is_running:
        return

    # Create the data payload with the new title and description
    data = {"title": new_title}

    # Use get_todo_id helper function to find the todo
    todo_id = get_todo_id(todo_title)

    # Send a PUT request to update the todo with the specified ID
    context.response = requests.put(f"{API_URL}/todos/{todo_id}", json=data)

    # Assert that the update was successful (status code should be 200)
    assert (
        context.response.status_code == 200
    ), f"Failed to update todo with id '{todo_id}'"


@then("the status code {status_code:d} will be received")
def step_impl(context, status_code):
    if not context.api_is_running:
        return
    assert (
        context.response.status_code == status_code
    ), f"Expected {status_code}, but got {context.response.status_code}"


@then("the response contains a list of todos")
def step_impl(context):
    if not context.api_is_running:
        return
    todos = context.response.json()
    assert "todos" in todos, "Response does not contain 'todos' key"


@then('the todo with title "{todo_name}" is included in the list')
def step_impl(context, todo_name):
    if not context.api_is_running:
        return
    todos = context.response.json()["todos"]
    assert any(
        todo["title"] == todo_name for todo in todos
    ), f"Todo with title '{todo_name}' not found in response"


@then(
    "the todo with has new title '{new_title}', doneStatus '{doneStatus}' and new description '{new_description}'"
)
def step_impl(context, new_title, doneStatus, new_description):
    if not context.api_is_running:
        return

    todo_id = get_todo_id(new_title)

    context.response = requests.get(f"{API_URL}/todos/{todo_id}")
    assert (
        context.response.status_code == 200
    ), f"Failed to retrieve todo with id '{todo_id}'"

    todo = context.response.json().get("todos", [])[0]

    # compare the value on the API to expected values
    assert (
        todo["title"] == new_title
    ), f"Expected title '{new_title}', but got '{todo['title']}'"
    assert (
        todo["doneStatus"] == doneStatus
    ), f"Expected description '{doneStatus}', but got '{todo['doneStatus']}'"
    assert (
        todo["description"] == new_description
    ), f"Expected description '{new_description}', but got '{todo['description']}'"

    print(
        f"Todo with id '{todo_id}' has the correct title, doneStatus and description."
    )


@then("the todo with has new title '{new_title}'")
def step_impl(context, new_title):
    if not context.api_is_running:
        return

    todo_id = get_todo_id(new_title)

    context.response = requests.get(f"{API_URL}/todos/{todo_id}")
    assert (
        context.response.status_code == 200
    ), f"Failed to retrieve todo with id '{todo_id}'"

    todo = context.response.json().get("todos", [])[0]

    assert (
        todo["title"] == new_title
    ), f"Expected title '{new_title}', but got '{todo['title']}'"

    print(f"Todo with id '{todo_id}' has the correct title.")


@then("only one todo with title '{todo_title}' should exist in the database")
def step_impl(context, todo_title):
    if not context.api_is_running:
        return

    response = requests.get(f"{API_URL}/todos")
    assert response.status_code == 200, "Failed to retrieve todos."

    # check the todos with the given todo_title, there should ONLY be one with this title if the other was deleted sucessfully
    todos_with_title = [
        todo for todo in response.json().get("todos", []) if todo["title"] == todo_title
    ]

    assert (
        len(todos_with_title) == 1
    ), f"Expected exactly one todo with title '{todo_title}', but found {len(todos_with_title)}."

    print(f"Only one todo with title '{todo_title}' exists in the database.")


@then("the response contains an empty list")
def step_impl(context):
    if not context.api_is_running:
        return
    todos = context.response.json()["todos"]
    assert len(todos) == 0, "Expected an empty list, but found some todos"


@then("the todo with title '{todo_title}' should no longer exist in the database")
def step_impl(context, todo_title):
    if not context.api_is_running:
        return

    todo_id = get_todo_id(todo_title)
    assert (
        todo_id is None
    ), "Todo with title '{todo_title}' still exists in the database."


@then("an error message '{error_message}' will be displayed")
def step_impl(context, error_message):
    if not context.api_is_running:
        return

    assert (
        error_message in context.response.text
    ), f"Expected error message '{error_message}' but got {context.response.text}"


@then(
    "the response contains categories '{category_titles}' for the todo with title '{todo_title}'"
)
def step_impl(context, category_titles, todo_title):
    if not context.api_is_running:
        return

    todo_id = get_todo_id(todo_title)
    assert todo_id is not None, f"Todo with title '{todo_title}' not found."

    category_response = requests.get(f"{API_URL}/todos/{todo_id}/categories")
    assert (
        category_response.status_code == 200
    ), f"Failed to retrieve categories for todo with ID {todo_id}."

    categories = [
        category["title"] for category in category_response.json().get("categories", [])
    ]

    # this function can take a LIST of categories or just one, purpose is to reduce number of step functions needed
    expected_categories = [title.strip() for title in category_titles.split(",")]

    for category in expected_categories:
        assert (
            category in categories
        ), f"Category '{category}' not found linked to todo '{todo_title}'."

    print(
        f"All expected categories {expected_categories} are linked to todo '{todo_title}'."
    )
