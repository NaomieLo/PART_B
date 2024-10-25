Feature: Delete Todo
  As a user managing my tasks, I want the ability to delete a todo by its title so I can keep my list organized and remove 
  items that are no longer relevant. This ensures my todo list only includes current tasks, helping me focus on what remains 
  to be done.

  Background:
    Given the API is responsive
    And there is an existing todo with title 'delete title' in the database

  # Normal Flow
  Scenario: Successfully delete a todo by title
    When the user deletes the todo with title 'delete title'
    Then the status code 200 will be received
    And the todo with title 'delete title' should no longer exist in the database

  # Alternate Flow
  Scenario: Successfully delete a todo by title when there are duplicate todo instances
    Given there is a second todo with title 'delete title' in the database
    When the user deletes the todo with title 'delete title'
    Then the status code 200 will be received
    And only one todo with title 'delete title' should exist in the database

  # Error Flow
  Scenario: Fail to delete a non-existent todo
    When the user attempts to delete a todo with id 10987654321
    Then the status code 404 will be received
    And an error message 'Could not find any instances with todos/10987654321' will be displayed
