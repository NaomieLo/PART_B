Feature: Post Categories to a Todo
  As a user, I want to add categories to a specific todo so that I can organize my tasks.

  Background:
    Given the API is responsive
    And there is an existing todo with title 'Workout' in the database

  # Normal Flow
  Scenario: Successfully post categories to a todo
    When the user posts the category 'Health' for the todo with title 'Workout'
    Then the status code 201 will be received
    And the response contains categories 'Health' for the todo with title 'Workout'

  # Alternate Flow
  Scenario: Post multiple categories to a todo
    Given the todo with title 'Workout' already has categories 'Fitness' and 'Leisure'
    When the user posts the category 'Health' for the todo with title 'Workout'
    Then the status code 201 will be received
    And the response contains categories 'Fitness, Leisure, Health' for the todo with title 'Workout'

  # Error Flow
  Scenario: Fail to post a category for a non-existent todo
    When the user attempts to post the category 'Fitness' for a non-existent todo
    Then the status code 404 will be received
    And an error message 'Could not find parent thing for relationship todos/9999/categories' will be displayed
