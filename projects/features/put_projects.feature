Feature: Update Project
  As a user, I want to update a project's details to keep my information current and relevant.

  Background:
    Given the API is responsive
    And there is an existing project with title 'Organized Project' in the database

  # Normal Flow
  Scenario: Successfully update a project with a new title and description
    When the user updates the project with title 'Organized Project' to have title 'Updated Title' and description 'Updated Description'
    Then the status code 200 will be received
    And the project with new title 'Updated Title' has new description 'Updated Description'

  # Alternate Flow
  Scenario: Update a project with only a new title
    When the user updates the project with title 'Organized Project' to have title 'Another Title'
    Then the status code 200 will be received
    And the project with title 'Another Title' should exist in the database

  # Error Flow
  Scenario: Fail to update a non-existent project
    When the user attempts to update a project with id 123456789
    Then the status code 404 will be received
    And an error message 'Invalid GUID for 123456789 entity project' will be displayed
