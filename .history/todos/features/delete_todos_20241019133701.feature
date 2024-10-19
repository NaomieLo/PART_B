Feature: Delete Todo
  As a user, I want to delete an existing todo so that I can remove tasks I no longer need.

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
    When the user attempts to delete a todo with id 9999
    Then the status code 404 will be received
    And an error message 'Could not find any instances with todos/9999' will be displayed
