Feature: Retrieve Todos
  As a user, I want to retrieve a comprehensive list of all my todos so that I can quickly see all my tasks and their 
  current statuses. This allows me to stay updated on what needs to be done across my todos and easily prioritize 
  or manage my tasks.

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
    And the response contains an empty list for 'todos'

  # Error Flow
  Scenario: Fail to retrieve a non-existent todo
    Given the API is responsive
    And the database contains several todos
    When the user attempts to retrieve a todo with id 10987654321
    Then the status code 404 will be received
    And an error message 'Could not find an instance with todos/10987654321' will be displayed
