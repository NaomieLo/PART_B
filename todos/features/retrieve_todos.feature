Feature: Retrieve Todos
  As a user, I want to retrieve a list of todos so that I can see all my tasks.

  Background:
    Given the API is responsive
    And the database contains several todos

  # Normal Flow
  Scenario Outline: Successfully retrieve all todos
    Given the API is responsive
    And the database contains several todos
    When the user retrieves all todos
    Then the status code 200 will be received
    And the response contains a list of todos
    And the todo with title "<todo_title>" is included in the list

    Examples:
      | todo_title          |
      | Grocery Shopping    |
      | Complete Homework   |
      | Pay Bills           |

  # Alternate Flow
  Scenario: Retrieve todos when there are no todos available
    Given the API is responsive
    And the database contains several todos
    Given the database is empty
    When the user retrieves all todos
    Then the status code 200 will be received
    And the response contains an empty list

  # Error Flow
  Scenario: Fail to retrieve a non-existent todo
    Given the API is responsive
    And the database contains several todos
    When the user attempts to retrieve a todo with id 9999
    Then the status code 404 will be received
    And an error message 'Could not find an instance with todos/9999' will be displayed
