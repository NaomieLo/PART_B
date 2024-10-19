Feature: Update Todo
  As a user, I want to retrieve the headers for all the categories linked to a specific todo so that I can quickly 
  assess the details of these categories without loading the full content.

  Background:
    Given the API is responsive
    And there is an existing todo with title 'Workout' in the database

  # Normal Flow
  Scenario: Successfully retrieve project items (tasksof) for a todo
    Given the todo with the title 'Workout' already has task items 'Morning Run' and 'Evening Stretch'
    When the user makes a GET request to /todos/:id/tasksof for the todo with the title 'Workout'
    Then the status code 200 will be received
    And the response will include all task items related to the todo, with each item having an ID, title, and description

  # Alternate Flow
  Scenario: Retrieve headers for a todo with no categories
    When the user makes a HEAD request to /todos/:id/categories for the todo with ID 1234 which has no categories linked
    Then the status code 200 will be received
    And the response will include headers like Content-Type and Content-Length with Content-Length set to 0

  # Error Flow
  Scenario: Fail to retrieve headers for categories of a non-existent todo
    When the user makes a HEAD request to /todos/:id/categories with a non-existent todo ID 9999
    Then the status code 404 will be received
    And an error message 'Todo with ID 9999 not found' will be displayed in the headers
