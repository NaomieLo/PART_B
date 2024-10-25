Feature: Update Todo
  As a user, I want to be able to update the details of an existing todo, including its title, 
  description, or status, so that I can keep my tasks accurate and reflect any changes in my plans. 
  This flexibility ensures my todo list remains up-to-date and relevant to my current goals.

  Background:
    Given the API is responsive
    And there is an existing todo with title 'Workout' in the database

  # Normal Flow
  Scenario: Successfully update a todo with a new title, done status, and description
    When the todo with title 'Workout' is updated with title 'Running', doneStatus 'true', and description 'Run 5 km'
    Then the status code 200 will be received
    And the todo with has new title 'Running', doneStatus 'true' and new description 'Run 5 km'

  # Alternate Flow
  Scenario: Successfully update a todo with only a new title
    When the todo with title 'Workout' is updated with title 'Lazy Day'
    Then the status code 200 will be received
    And the todo with has new title 'Lazy Day'

  # Error Flow
  Scenario: Fail to update a non-existent todo
    When the user attempts to update a todo with a non-existent todo
    Then the status code 404 will be received
    And an error message 'Invalid GUID for 10987654321 entity todo' will be displayed
