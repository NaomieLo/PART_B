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
    And the response of the todo with title 'Workout' will include the project with title 'Morning Run' and 'Evening Stretch'

  # Alternate Flow
  Scenario: Retrieve project items for a todo with no tasksof
    Given the todo with the title 'Workout' has no tasks instances 
    When the user makes a GET request to /todos/:id/tasksof for the todo with the title 'Workout'
    Then the status code 200 will be received
    And the response contains an empty list for 'projects'

  
  # Error Flow
  Scenario: Fail to retrieve project items for a non-existent todo
    When the user attempts to retrieve a taskof with a todo with id 9999
    Then the status code 404 will be received
    And the response contains empty list for 'projects' with id '9999'
